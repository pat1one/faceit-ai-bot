// Optimized API client with caching and request deduplication

import { cacheManager, withCache } from "./cache";

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: any;
  cache?: boolean;
  cacheTTL?: number;
}

class APIClient {
  private baseURL: string;
  private pendingRequests: Map<string, Promise<any>> = new Map();

  constructor(baseURL: string = "") {
    this.baseURL = baseURL || this.getApiUrl();
  }

  private getApiUrl(): string {
    if (typeof window === "undefined") {
      return "http://localhost:8000";
    }

    if (window.location.hostname === "localhost") {
      return "http://localhost:8000";
    }

    return `https://${window.location.hostname}`;
  }

  private getCacheKey(url: string, options?: RequestOptions): string {
    return `${options?.method || "GET"}:${url}`;
  }

  private async dedupRequest<T>(
    key: string,
    fetcher: () => Promise<T>
  ): Promise<T> {
    if (this.pendingRequests.has(key)) {
      return this.pendingRequests.get(key)!;
    }

    const promise = fetcher().finally(() => {
      this.pendingRequests.delete(key);
    });

    this.pendingRequests.set(key, promise);
    return promise;
  }

  async get<T>(
    url: string,
    options?: RequestOptions & { cache?: boolean; cacheTTL?: number }
  ): Promise<T> {
    const cacheKey = this.getCacheKey(url, { method: "GET" });

    if (options?.cache !== false) {
      return withCache(cacheKey, () => this.request<T>(url, options), options?.cacheTTL);
    }

    return this.request<T>(url, options);
  }

  async post<T>(url: string, options?: RequestOptions): Promise<T> {
    cacheManager.invalidatePattern(`GET:${url.split("?")[0]}`);
    return this.request<T>(url, { ...options, method: "POST" });
  }

  async put<T>(url: string, options?: RequestOptions): Promise<T> {
    cacheManager.invalidatePattern(`GET:${url.split("?")[0]}`);
    return this.request<T>(url, { ...options, method: "PUT" });
  }

  async delete<T>(url: string, options?: RequestOptions): Promise<T> {
    cacheManager.invalidatePattern(`GET:${url.split("?")[0]}`);
    return this.request<T>(url, { ...options, method: "DELETE" });
  }

  private async request<T>(url: string, options?: RequestOptions): Promise<T> {
    const fullURL = `${this.baseURL}${url}`;
    const method = options?.method || "GET";
    const cacheKey = `${method}:${url}`;

    return this.dedupRequest(cacheKey, async () => {
      const response = await fetch(fullURL, {
        method,
        headers: {
          "Content-Type": "application/json",
          ...options?.headers,
        },
        body: options?.body ? JSON.stringify(options.body) : undefined,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      return response.json() as Promise<T>;
    });
  }
}

export const apiClient = new APIClient();

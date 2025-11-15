# Faceit AI Bot Architecture

## System Architecture Overview

```mermaid
graph TB
    %% External Users
    Users[Users] --> HTTPS[HTTPS/TLS]
    
    %% Load Balancer
    HTTPS --> LB[Nginx Load Balancer]
    
    %% Frontend
    LB --> Frontend[Next.js Frontend]
    Frontend --> API[API Gateway]
    
    %% Backend Services
    API --> Auth[Auth Service]
    API --> AI[AI Analysis Service]
    API --> Payment[Payment Service]
    
    %% Database Layer
    Auth --> DB[(PostgreSQL)]
    AI --> DB
    Payment --> DB
    
    %% Cache Layer
    Auth --> Redis[(Redis Cache)]
    AI --> Redis
    
    %% Background Jobs
    AI --> Celery[Celery Workers]
    Celery --> Redis
    
    %% External APIs
    AI --> Faceit[Faceit API]
    
    %% Monitoring
    LB --> Prometheus[Prometheus]
    API --> Prometheus
    Auth --> Prometheus
    AI --> Prometheus
    
    Prometheus --> Grafana[Grafana]
    Prometheus --> AlertManager[AlertManager]
    
    %% Logging
    Frontend --> Loki[Loki]
    API --> Loki
    Auth --> Loki
    AI --> Loki
    
    %% Error Tracking
    API --> Sentry[Sentry]
    Auth --> Sentry
    AI --> Sentry
    
    %% Styling
    classDef frontend fill:#61dafb,stroke:#2196f3,color:#000
    classDef backend fill:#68a063,stroke:#4caf50,color:#fff
    classDef database fill:#ff5722,stroke:#f44336,color:#fff
    classDef monitoring fill:#9c27b0,stroke:#673ab7,color:#fff
    classDef external fill:#ff9800,stroke:#ff5722,color:#fff
    
    class Users,HTTPS,Frontend frontend
    class API,Auth,AI,Payment,Celery backend
    class DB,Redis database
    class Prometheus,Grafana,AlertManager,Loki,Sentry monitoring
    class LB,Faceit external
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Auth
    participant AI
    participant DB
    participant Redis
    participant FaceitAPI
    
    User->>Frontend: Login Request
    Frontend->>API: POST /api/auth/login
    API->>Auth: Validate Credentials
    Auth->>DB: Check User
    DB-->>Auth: User Data
    Auth-->>API: JWT Token
    API-->>Frontend: Auth Response
    Frontend-->>User: Dashboard
    
    User->>Frontend: Request Analysis
    Frontend->>API: POST /api/analysis/analyze
    API->>Auth: Validate Token
    Auth->>Redis: Check Cache
    Redis-->>Auth: Token Valid
    Auth-->>API: User Info
    
    API->>AI: Process Analysis
    AI->>FaceitAPI: Fetch Player Stats
    FaceitAPI-->>AI: Player Data
    AI->>DB: Store Results
    AI-->>API: Analysis Results
    API-->>Frontend: Response
    Frontend-->>User: Display Analysis
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Web Server"
            Nginx[Nginx Reverse Proxy]
            SSL[SSL/TLS Certificates]
        end
        
        subgraph "Application Layer"
            Frontend[Next.js App :3000]
            Backend[FastAPI :8000]
            Workers[Celery Workers]
        end
        
        subgraph "Data Layer"
            PostgreSQL[(PostgreSQL :5432)]
            Redis[(Redis :6379)]
        end
        
        subgraph "Monitoring Stack"
            Prometheus[Prometheus :9090]
            Grafana[Grafana :3001]
            Loki[Loki :3100]
            AlertManager[AlertManager :9093]
        end
    end
    
    subgraph "External Services"
        Faceit[Faceit API]
        Sentry[Sentry.io]
        Cloud[Cloud Storage]
    end
    
    %% Connections
    Nginx --> Frontend
    Nginx --> Backend
    Backend --> PostgreSQL
    Backend --> Redis
    Workers --> Redis
    Backend --> Faceit
    Backend --> Sentry
    
    %% Monitoring
    Frontend --> Prometheus
    Backend --> Prometheus
    Workers --> Prometheus
    Prometheus --> Grafana
    Prometheus --> AlertManager
    
    %% Logging
    Frontend --> Loki
    Backend --> Loki
    Workers --> Loki
    
    %% Styling
    classDef server fill:#2196f3,color:#fff
    classDef app fill:#4caf50,color:#fff
    classDef data fill:#ff5722,color:#fff
    classDef monitor fill:#9c27b0,color:#fff
    classDef external fill:#ff9800,color:#fff
    
    class Nginx,SSL server
    class Frontend,Backend,Workers app
    class PostgreSQL,Redis data
    class Prometheus,Grafana,Loki,AlertManager monitor
    class Faceit,Sentry,Cloud external
```

## Service Communication

```mermaid
graph LR
    subgraph "Frontend Services"
        Web[Next.js Web App]
        Mobile[Mobile App]
    end
    
    subgraph "API Gateway"
        Gateway[API Gateway]
    end
    
    subgraph "Microservices"
        AuthSrv[Auth Service]
        AISrv[AI Analysis Service]
        PaymentSrv[Payment Service]
        NotificationSrv[Notification Service]
    end
    
    subgraph "Infrastructure"
        PostgreSQL[(PostgreSQL)]
        Redis[(Redis)]
        Queue[Message Queue]
        Storage[File Storage]
    end
    
    subgraph "External APIs"
        FaceitAPI[Faceit API]
        PaymentProvider[Payment Gateway]
        EmailService[Email Service]
    end
    
    %% Service Connections
    Web --> Gateway
    Mobile --> Gateway
    
    Gateway --> AuthSrv
    Gateway --> AISrv
    Gateway --> PaymentSrv
    Gateway --> NotificationSrv
    
    AuthSrv --> PostgreSQL
    AuthSrv --> Redis
    
    AISrv --> PostgreSQL
    AISrv --> Redis
    AISrv --> Queue
    AISrv --> FaceitAPI
    
    PaymentSrv --> PostgreSQL
    PaymentSrv --> PaymentProvider
    
    NotificationSrv --> Queue
    NotificationSrv --> EmailService
    
    Queue --> Storage
    
    %% Styling
    classDef frontend fill:#61dafb,color:#000
    classDef gateway fill:#2196f3,color:#fff
    classDef service fill:#4caf50,color:#fff
    classDef infra fill:#ff5722,color:#fff
    classDef external fill:#ff9800,color:#fff
    
    class Web,Mobile frontend
    class Gateway gateway
    class AuthSrv,AISrv,PaymentSrv,NotificationSrv service
    class PostgreSQL,Redis,Queue,Storage infra
    class FaceitAPI,PaymentProvider,EmailService external
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Network Security"
            WAF[Web Application Firewall]
            DDoS[DDoS Protection]
            SSL[TLS/SSL Encryption]
        end
        
        subgraph "Application Security"
            Auth[JWT Authentication]
            RBAC[Role-Based Access Control]
            RateLimit[Rate Limiting]
            CORS[CORS Policy]
        end
        
        subgraph "Data Security"
            Encryption[Data Encryption]
            Hashing[Password Hashing]
            Secrets[Secret Management]
        end
        
        subgraph "Monitoring Security"
            Audit[Audit Logging]
            Alerts[Security Alerts]
            Scanning[Vulnerability Scanning]
        end
    end
    
    subgraph "Protected Resources"
        API[API Endpoints]
        DB[(Database)]
        Files[File Storage]
        Cache[(Redis Cache)]
    end
    
    %% Security Flow
    WAF --> SSL
    SSL --> Auth
    Auth --> RBAC
    RBAC --> RateLimit
    RateLimit --> CORS
    CORS --> API
    
    API --> Encryption
    Encryption --> DB
    API --> Hashing
    Hashing --> DB
    
    API --> Secrets
    Secrets --> Cache
    API --> Files
    
    %% Monitoring
    Auth --> Audit
    RBAC --> Audit
    API --> Audit
    Audit --> Alerts
    Scanning --> Alerts
    
    %% Styling
    classDef network fill:#2196f3,color:#fff
    classDef app fill:#4caf50,color:#fff
    classDef data fill:#ff5722,color:#fff
    classDef monitor fill:#9c27b0,color:#fff
    classDef resource fill:#ff9800,color:#fff
    
    class WAF,DDoS,SSL network
    class Auth,RBAC,RateLimit,CORS app
    class Encryption,Hashing,Secrets data
    class Audit,Alerts,Scanning monitor
    class API,DB,Files,Cache resource
```

## CI/CD Pipeline Architecture

```mermaid
graph LR
    subgraph "Development"
        Dev[Local Development]
        IDE[IDE/Editor]
        Git[Git Repository]
    end
    
    subgraph "CI/CD Pipeline"
        subgraph "Continuous Integration"
            Trigger[Git Push Trigger]
            Build[Build & Test]
            Security[Security Scan]
            Quality[Code Quality]
        end
        
        subgraph "Continuous Deployment"
            Staging[Staging Deploy]
            Integration[Integration Tests]
            Production[Production Deploy]
            Monitoring[Health Checks]
        end
    end
    
    subgraph "Environments"
        DevEnv[Development Environment]
        StageEnv[Staging Environment]
        ProdEnv[Production Environment]
    end
    
    subgraph "Infrastructure"
        Docker[Docker Registry]
        K8s[Kubernetes Cluster]
        Monitoring[Monitoring Stack]
    end
    
    %% Pipeline Flow
    Dev --> Git
    IDE --> Git
    Git --> Trigger
    
    Trigger --> Build
    Build --> Security
    Security --> Quality
    Quality --> Staging
    
    Staging --> Integration
    Integration --> Production
    Production --> Monitoring
    
    %% Environment Connections
    Build --> DevEnv
    Staging --> StageEnv
    Production --> ProdEnv
    
    %% Infrastructure
    Build --> Docker
    Staging --> K8s
    Production --> K8s
    Monitoring --> K8s
    
    %% Styling
    classDef dev fill:#61dafb,color:#000
    classDef pipeline fill:#4caf50,color:#fff
    classDef env fill:#ff5722,color:#fff
    classDef infra fill:#9c27b0,color:#fff
    
    class Dev,IDE,Git dev
    class Trigger,Build,Security,Quality,Staging,Integration,Production,Monitoring pipeline
    class DevEnv,StageEnv,ProdEnv env
    class Docker,K8s,Monitoring infra
```

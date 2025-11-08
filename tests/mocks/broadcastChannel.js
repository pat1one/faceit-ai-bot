class MockBroadcastChannel {
  constructor(name) {
    this.name = name;
  }
  postMessage(data) {}
  addEventListener(type, listener) {}
  removeEventListener(type, listener) {}
  close() {}
}

module.exports = { MockBroadcastChannel };
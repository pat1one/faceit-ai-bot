import '@testing-library/jest-dom';
import 'whatwg-fetch';

const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

console.log('setupTests.ts loaded without MSW');
console.log('Matchers loaded:', typeof expect !== 'undefined' && typeof expect.extend !== 'undefined');
console.log('TextEncoder in setupTests:', typeof global.TextEncoder);
console.log('Global TextEncoder:', global.TextEncoder);
console.log('Global TextDecoder:', global.TextDecoder);

module.exports = {
  preset: "ts-jest",
  testEnvironment: "jest-fixed-jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/tests/jest.setup.ts"],
  transformIgnorePatterns: [
    "node_modules/(?!@bundled-es-modules)/",
    "node_modules/(?!variables/.*)",
  ],
  moduleNameMapper: {
    "\\.(css|scss)$": "<rootDir>/src/tests/mocks/files/styleMock.js",
  },
};

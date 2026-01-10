import { resumeApi, jobsApi, optimizationApi, exportApi } from './api';

// Mock axios instead of fetch to avoid jsdom issues
vi.mock('axios', () => ({
  default: {
    create: () => ({
      post: vi.fn(),
      get: vi.fn(),
    }),
  },
}));

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('resumeApi', () => {
    it('has uploadResume method', () => {
      expect(typeof resumeApi.uploadResume).toBe('function');
    });
  });

  describe('jobsApi', () => {
    it('has analyzeJob method', () => {
      expect(typeof jobsApi.analyzeJob).toBe('function');
    });
  });

  describe('optimizationApi', () => {
    it('has startOptimization method', () => {
      expect(typeof optimizationApi.startOptimization).toBe('function');
    });

    it('has generateCoverLetter method', () => {
      expect(typeof optimizationApi.generateCoverLetter).toBe('function');
    });

    it('has saveOptimization method', () => {
      expect(typeof optimizationApi.saveOptimization).toBe('function');
    });
  });

  describe('exportApi', () => {
    it('has exportResume method', () => {
      expect(typeof exportApi.exportResume).toBe('function');
    });
  });
});
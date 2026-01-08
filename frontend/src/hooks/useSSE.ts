import { useState, useEffect, useRef } from 'react';
import { OptimizationProgress } from '@/types';

interface UseSSEOptions {
  // eslint-disable-next-line no-unused-vars
  onProgress?: (progress: OptimizationProgress) => void;
  // eslint-disable-next-line no-unused-vars
  onError?: (error: Event) => void;
  onComplete?: () => void;
}

export const useSSE = (url: string | null, options: UseSSEOptions = {}) => {
  const [events, setEvents] = useState<OptimizationProgress[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!url) return;

    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;
    setIsConnected(true);
    setError(null);

    eventSource.onmessage = (event) => {
      try {
        const progress: OptimizationProgress = JSON.parse(event.data);
        
        setEvents(prev => [...prev, progress]);
        options.onProgress?.(progress);

        if (progress.completed) {
          options.onComplete?.();
          eventSource.close();
          setIsConnected(false);
        }
      } catch (err) {
        console.error('Failed to parse SSE event:', err);
      }
    };

    eventSource.onerror = (event) => {
      setError('Connection error occurred');
      setIsConnected(false);
      options.onError?.(event);
      eventSource.close();
    };

    return () => {
      eventSource.close();
      setIsConnected(false);
    };
  }, [url]);

  const disconnect = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      setIsConnected(false);
    }
  };

  return {
    events,
    isConnected,
    error,
    disconnect,
  };
};
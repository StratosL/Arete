import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ErrorBoundary } from './ErrorBoundary';

// Component that throws an error for testing
const ThrowError = ({ shouldThrow }: { shouldThrow: boolean }) => {
  if (shouldThrow) {
    throw new Error('Test error message');
  }
  return <div>No error</div>;
};

// Custom fallback component for testing
const CustomFallback = ({ error, resetError }: { error?: Error; resetError: () => void }) => (
  <div>
    <h2>Custom Error Fallback</h2>
    <p>Error: {error?.message}</p>
    <button onClick={resetError}>Custom Reset</button>
  </div>
);

describe('ErrorBoundary', () => {
  // Suppress console.error for these tests
  const originalError = console.error;
  beforeAll(() => {
    console.error = vi.fn();
  });
  afterAll(() => {
    console.error = originalError;
  });

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={false} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('No error')).toBeInTheDocument();
  });

  it('renders default error fallback when error occurs', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('Test error message')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
  });

  it('renders custom fallback when provided', () => {
    render(
      <ErrorBoundary fallback={CustomFallback}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Custom Error Fallback')).toBeInTheDocument();
    expect(screen.getByText('Error: Test error message')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /custom reset/i })).toBeInTheDocument();
  });

  it('resets error state when reset button is clicked', async () => {
    const user = userEvent.setup();
    
    const TestComponent = () => {
      const [shouldThrow, setShouldThrow] = React.useState(true);
      
      React.useEffect(() => {
        // Reset the error state after a short delay to simulate recovery
        const timer = setTimeout(() => setShouldThrow(false), 100);
        return () => clearTimeout(timer);
      }, []);
      
      return <ThrowError shouldThrow={shouldThrow} />;
    };
    
    render(
      <ErrorBoundary>
        <TestComponent />
      </ErrorBoundary>
    );
    
    // Should show error initially
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    
    // Click reset button
    const resetButton = screen.getByRole('button', { name: /try again/i });
    await user.click(resetButton);
    
    // Should show children again
    expect(screen.getByText('No error')).toBeInTheDocument();
  });

  it('handles errors without message', () => {
    const ThrowErrorWithoutMessage = () => {
      throw new Error();
    };
    
    render(
      <ErrorBoundary>
        <ThrowErrorWithoutMessage />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('An unexpected error occurred')).toBeInTheDocument();
  });

  it('logs error details to console', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );
    
    expect(consoleSpy).toHaveBeenCalledWith('ErrorBoundary caught error:', expect.any(Error));
    expect(consoleSpy).toHaveBeenCalledWith('ErrorBoundary details:', expect.objectContaining({
      error: expect.any(Error),
      errorInfo: expect.any(Object)
    }));
    
    consoleSpy.mockRestore();
  });

  it('resets error state with custom fallback', async () => {
    const user = userEvent.setup();
    
    const TestComponent = () => {
      const [shouldThrow, setShouldThrow] = React.useState(true);
      
      React.useEffect(() => {
        const timer = setTimeout(() => setShouldThrow(false), 100);
        return () => clearTimeout(timer);
      }, []);
      
      return <ThrowError shouldThrow={shouldThrow} />;
    };
    
    render(
      <ErrorBoundary fallback={CustomFallback}>
        <TestComponent />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Custom Error Fallback')).toBeInTheDocument();
    
    const resetButton = screen.getByRole('button', { name: /custom reset/i });
    await user.click(resetButton);
    
    expect(screen.getByText('No error')).toBeInTheDocument();
  });

  it('handles multiple error resets', async () => {
    const user = userEvent.setup();
    
    const TestComponent = ({ throwCount }: { throwCount: number }) => {
      if (throwCount > 0) {
        throw new Error(`Error ${throwCount}`);
      }
      return <div>Success after {throwCount} errors</div>;
    };
    
    let throwCount = 2;
    const { rerender } = render(
      <ErrorBoundary>
        <TestComponent throwCount={throwCount} />
      </ErrorBoundary>
    );
    
    // First error
    expect(screen.getByText('Error 2')).toBeInTheDocument();
    
    const resetButton = screen.getByRole('button', { name: /try again/i });
    await user.click(resetButton);
    
    // Simulate component update with different error
    throwCount = 1;
    rerender(
      <ErrorBoundary>
        <TestComponent throwCount={throwCount} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Error 1')).toBeInTheDocument();
    
    await user.click(resetButton);
    
    // Finally success
    throwCount = 0;
    rerender(
      <ErrorBoundary>
        <TestComponent throwCount={throwCount} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Success after 0 errors')).toBeInTheDocument();
  });
});
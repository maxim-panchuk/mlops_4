from src.pipeline import Pipeline

if __name__ == "__main__":
    # Create and run pipeline
    pipeline = Pipeline()
    results = pipeline.run()
    
    # Print evaluation results
    print("\nModel Evaluation Results:")
    print(f"Accuracy: {results['accuracy']:.4f}")
    print("\nClassification Report:")
    for key, value in results.items():
        if key != 'accuracy':
            print(f"{key}: {value}")
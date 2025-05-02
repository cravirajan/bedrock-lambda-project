# import json
# import os
# import boto3
# from lambda_function import lambda_handler

# def test_locally():
#     # Check if AWS credentials are available
#     session = boto3.Session()
#     credentials = session.get_credentials()
#     if not credentials:
#         print("Error: AWS credentials not found. Please configure your AWS credentials.")
#         print("You can use the AWS Toolkit in VS Code or run 'aws configure' in the terminal.")
#         return
    
#     print(f"Using AWS profile: {session.profile_name or 'default'}")
#     print(f"Using region: {session.region_name or os.environ.get('AWS_REGION', 'us-east-1')}")
    
#     try:
#         # Load test event
#         with open('events/test-event.json', 'r') as f:
#             event = json.load(f)
        
#         print("\nInvoking Lambda function with test event...")
#         response = lambda_handler(event, None)
        
#         # Parse and pretty print the response
#         print("\nResponse:")
#         status_code = response.get('statusCode')
#         print(f"Status code: {status_code}")
        
#         if status_code == 200:
#             body = json.loads(response.get('body', '{}'))
#             print("\nSummary:")
#             print(body.get('summary'))
#             print(f"\nEmbedding dimension: {body.get('embedding_dimension')}")
#         else:
#             body = json.loads(response.get('body', '{}'))
#             print(f"Error: {body.get('error', 'Unknown error')}")
            
#     except Exception as e:
#         print(f"Error during local testing: {str(e)}")

# if __name__ == "__main__":
#     test_locally()







# import json
# import os
# import boto3
# import time
# import logging
# from lambda_function import lambda_handler

# # Configure logging
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger("bedrock-test")

# def test_locally():
#     """Test the Lambda function locally using AWS credentials from your profile"""
#     logger.info("Starting local test of the Lambda function")
#     start_time = time.time()
    
#     # Check if AWS credentials are available
#     logger.info("Checking AWS credentials")
#     session = boto3.Session()
#     credentials = session.get_credentials()
    
#     if not credentials:
#         logger.error("AWS credentials not found. Please configure your AWS credentials.")
#         logger.error("You can use the AWS Toolkit in VS Code or run 'aws configure' in the terminal.")
#         return
    
#     logger.info(f"Using AWS profile: {session.profile_name or 'default'}")
#     logger.info(f"Using region: {session.region_name or os.environ.get('AWS_REGION', 'us-east-1')}")
    
#     try:
#         # Load test event
#         event_path = 'events/test-event.json'
#         logger.info(f"Loading test event from {event_path}")
        
#         with open(event_path, 'r') as f:
#             event = json.load(f)
            
#         logger.info(f"Test event loaded: {json.dumps(event)}")
#         logger.info(f"Query: '{event.get('query', 'N/A')}'")
#         logger.info(f"Text length: {len(event.get('text', ''))}")
        
#         # Invoke Lambda function
#         logger.info("Invoking Lambda handler with test event...")
#         response = lambda_handler(event, None)
        
#         # Parse and print the response
#         logger.info("Processing response")
#         status_code = response.get('statusCode')
#         logger.info(f"Status code: {status_code}")
        
#         if status_code == 200:
#             body = json.loads(response.get('body', '{}'))
            
#             logger.info("\n" + "="*80)
#             logger.info("SUMMARY RESULTS")
#             logger.info("="*80)
#             print("\n" + body.get('summary') + "\n")
#             logger.info("="*80)
            
#             logger.info(f"Embedding dimension: {body.get('embedding_dimension')}")
#             logger.info(f"Processing time: {body.get('processing_time_seconds')} seconds")
#         else:
#             body = json.loads(response.get('body', '{}'))
#             logger.error(f"Error: {body.get('error', 'Unknown error')}")
            
#         end_time = time.time()
#         logger.info(f"Local test completed in {end_time - start_time:.2f} seconds")
        
#     except FileNotFoundError:
#         logger.error(f"Test event file not found: {event_path}")
#         logger.error("Please create the events directory and add a test-event.json file")
#     except json.JSONDecodeError:
#         logger.error(f"Invalid JSON in test event file: {event_path}")
#     except Exception as e:
#         logger.error(f"Error during local testing: {str(e)}", exc_info=True)

# if __name__ == "__main__":
#     test_locally()

















import json
import os
import boto3
import time
import logging
import pickle
from pathlib import Path
from lambda_function import lambda_handler, CACHE_DIR, CACHE_FILE, load_embedding_cache

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("bedrock-test")

def test_locally():
    """Test the Lambda function locally using AWS credentials from your profile"""
    logger.info("Starting local test of the Lambda function")
    start_time = time.time()
    
    # Check if cache directory exists
    cache_path = Path(CACHE_DIR)
    cache_file = Path(CACHE_FILE)
    
    if not cache_path.exists():
        logger.info(f"Creating cache directory: {CACHE_DIR}")
        cache_path.mkdir(parents=True, exist_ok=True)
    else:
        logger.info(f"Using existing cache directory: {CACHE_DIR}")
    
    # Check cache file
    if cache_file.exists():
        try:
            with open(CACHE_FILE, 'rb') as f:
                cache = pickle.load(f)
            logger.info(f"Cache file found with {len(cache)} entries")
            logger.info(f"Cache file size: {cache_file.stat().st_size / 1024:.2f} KB")
        except Exception as e:
            logger.warning(f"Error reading cache file: {str(e)}")
    else:
        logger.info("No cache file found - will be created if needed")
    
    # Check if AWS credentials are available
    logger.info("Checking AWS credentials")
    session = boto3.Session()
    credentials = session.get_credentials()
    
    if not credentials:
        logger.error("AWS credentials not found. Please configure your AWS credentials.")
        logger.error("You can use the AWS Toolkit in VS Code or run 'aws configure' in the terminal.")
        return
    
    logger.info(f"Using AWS profile: {session.profile_name or 'default'}")
    logger.info(f"Using region: {session.region_name or os.environ.get('AWS_REGION', 'us-east-1')}")
    
    try:
        # Load test event
        event_path = 'events/test-event.json'
        logger.info(f"Loading test event from {event_path}")
        
        with open(event_path, 'r') as f:
            event = json.load(f)
            
        logger.info(f"Test event loaded: {json.dumps(event)}")
        logger.info(f"Query: '{event.get('query', 'N/A')}'")
        logger.info(f"Text length: {len(event.get('text', ''))}")
        
        # Invoke Lambda function
        logger.info("Invoking Lambda handler with test event...")
        response = lambda_handler(event, None)
        
        # Parse and print the response
        logger.info("Processing response")
        status_code = response.get('statusCode')
        logger.info(f"Status code: {status_code}")
        
        if status_code == 200:
            body = json.loads(response.get('body', '{}'))
            
            logger.info("\n" + "="*80)
            logger.info("SUMMARY RESULTS")
            logger.info("="*80)
            print("\n" + body.get('summary') + "\n")
            logger.info("="*80)
            
            logger.info(f"Embedding dimension: {body.get('embedding_dimension')}")
            logger.info(f"Embedding source: {body.get('embedding_source')}")
            logger.info(f"Processing time: {body.get('processing_time_seconds')} seconds")
            
            # Cache management options
            print("\nCache Management Options:")
            print("1. Clear embedding cache")
            print("2. Show cache statistics")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '1':
                clear_cache()
            elif choice == '2':
                show_cache_stats()
            
        else:
            body = json.loads(response.get('body', '{}'))
            logger.error(f"Error: {body.get('error', 'Unknown error')}")
            
        end_time = time.time()
        logger.info(f"Local test completed in {end_time - start_time:.2f} seconds")
        
    except FileNotFoundError:
        logger.error(f"Test event file not found: {event_path}")
        logger.error("Please create the events directory and add a test-event.json file")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in test event file: {event_path}")
    except Exception as e:
        logger.error(f"Error during local testing: {str(e)}", exc_info=True)

def clear_cache():
    """Clear the embedding cache"""
    try:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            logger.info(f"Cache file deleted: {CACHE_FILE}")
        else:
            logger.info("No cache file to delete")
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")

def show_cache_stats():
    """Show statistics about the embedding cache"""
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("No cache file found")
            return
            
        with open(CACHE_FILE, 'rb') as f:
            cache = pickle.load(f)
            
        file_size = os.path.getsize(CACHE_FILE) / 1024  # KB
        
        logger.info("\nCache Statistics:")
        logger.info(f"Total entries: {len(cache)}")
        logger.info(f"File size: {file_size:.2f} KB")
        
        if cache:
            # Get a sample embedding to check dimension
            sample_key = next(iter(cache))
            sample_embedding = cache[sample_key]
            logger.info(f"Embedding dimension: {len(sample_embedding)}")
            
    except Exception as e:
        logger.error(f"Error showing cache stats: {str(e)}")

if __name__ == "__main__":
    test_locally()
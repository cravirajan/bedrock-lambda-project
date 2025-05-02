# import boto3
# import json
# import os
# from typing import Dict, Any, List

# # Initialize Bedrock client
# # The credentials will be automatically picked up from your AWS profile
# bedrock = boto3.client(
#     service_name='bedrock-runtime',
#     region_name=os.environ.get('AWS_REGION', 'us-east-1')
# )

# # Constants for models
# CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
# TITAN_EMBEDDINGS_MODEL_ID = "amazon.titan-embed-text-v1"

# def get_embeddings(text: str) -> List[float]:
#     """Generate embeddings for the given text using Titan Embeddings model"""
#     try:
#         response = bedrock.invoke_model(
#             modelId=TITAN_EMBEDDINGS_MODEL_ID,
#             body=json.dumps({
#                 "inputText": text
#             })
#         )
#         response_body = json.loads(response['body'].read().decode('utf-8'))
#         return response_body['embedding']
#     except Exception as e:
#         print(f"Error generating embeddings: {str(e)}")
#         raise

# def generate_summary(text: str, query: str) -> str:
#     """Generate summary using Claude model"""
#     try:
#         prompt = f"""
#         I need you to summarize the following text based on this query: "{query}"
        
#         Text to summarize:
#         {text}
        
#         Please provide a concise and relevant summary focusing on aspects related to the query.
#         """
        
#         response = bedrock.invoke_model(
#             modelId=CLAUDE_MODEL_ID,
#             body=json.dumps({
#                 "anthropic_version": "bedrock-2023-05-31",
#                 "max_tokens": 1000,
#                 "temperature":0,
#                 "messages": [
#                     {
#                         "role": "user",
#                         "content": prompt
#                     }
#                 ]
#             })
#         )
#         response_body = json.loads(response['body'].read().decode('utf-8'))
#         return response_body['content'][0]['text']
#     except Exception as e:
#         print(f"Error generating summary: {str(e)}")
#         raise

# def lambda_handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
#     """Lambda function handler"""
#     try:
#         # Extract the text and query from the event
#         text = event.get('text', '')
#         query = event.get('query', '')
        
#         if not text or not query:
#             return {
#                 'statusCode': 400,
#                 'body': json.dumps({'error': 'Missing text or query parameter'})
#             }
        
#         # Generate embeddings for the text (optional - can be used for similarity/retrieval)
#         embeddings = get_embeddings(text)
        
#         # Generate summary based on the query
#         summary = generate_summary(text, query)
        
#         return {
#             'statusCode': 200,
#             'body': json.dumps({
#                 'summary': summary,
#                 'embedding_dimension': len(embeddings),
#                 # 'embeddings': embeddings  # Commented out as embeddings can be large
#             })
#         }
#     except Exception as e:
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)})
#         }



# Updated Code with Enhanced Logging for Lambda Function and Local Testing

# import boto3
# import json
# import os
# import time
# import logging
# from typing import Dict, Any, List

# # Configure logging
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger("bedrock-summarizer")

# # Initialize Bedrock client
# # The credentials will be automatically picked up from your AWS profile
# logger.info("Initializing Bedrock client")
# bedrock = boto3.client(
#     service_name='bedrock-runtime',
#     region_name=os.environ.get('AWS_REGION', 'us-east-1')
# )
# logger.info(f"Bedrock client initialized for region: {os.environ.get('AWS_REGION', 'us-east-1')}")

# # Constants for models
# CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
# TITAN_EMBEDDINGS_MODEL_ID = "amazon.titan-embed-text-v1"
# logger.info(f"Using Claude model: {CLAUDE_MODEL_ID}")
# logger.info(f"Using Embeddings model: {TITAN_EMBEDDINGS_MODEL_ID}")

# def get_embeddings(text: str) -> List[float]:
#     """Generate embeddings for the given text using Titan Embeddings model"""
#     start_time = time.time()
#     logger.info("Starting embedding generation with Titan Embeddings model")
    
#     try:
#         logger.info(f"Preparing request for text of length: {len(text)} characters")
#         response = bedrock.invoke_model(
#             modelId=TITAN_EMBEDDINGS_MODEL_ID,
#             body=json.dumps({
#                 "inputText": text
#             })
#         )
#         logger.info("Received response from Titan Embeddings model")
        
#         response_body = json.loads(response['body'].read().decode('utf-8'))
#         embeddings = response_body['embedding']
        
#         end_time = time.time()
#         logger.info(f"Embedding generation completed in {end_time - start_time:.2f} seconds")
#         logger.info(f"Generated embeddings with dimension: {len(embeddings)}")
        
#         return embeddings
#     except Exception as e:
#         logger.error(f"Error generating embeddings: {str(e)}")
#         raise

# def generate_summary(text: str, query: str) -> str:
#     """Generate summary using Claude model"""
#     start_time = time.time()
#     logger.info(f"Starting summary generation with Claude model")
#     logger.info(f"Query: '{query}'")
#     logger.info(f"Input text length: {len(text)} characters")
    
#     try:
#         prompt = f"""
#         I need you to summarize the following text based on this query: "{query}"
        
#         Text to summarize:
#         {text}
        
#         Please provide a concise and relevant summary focusing on aspects related to the query.
#         """
        
#         logger.info("Preparing request for Claude model")
#         response = bedrock.invoke_model(
#             modelId=CLAUDE_MODEL_ID,
#             body=json.dumps({
#                 "anthropic_version": "bedrock-2023-05-31",
#                 "max_tokens": 1000,
#                 "temperature": 0,
#                 "messages": [
#                     {
#                         "role": "user",
#                         "content": prompt
#                     }
#                 ]
#             })
#         )
#         logger.info("Received response from Claude model")
        
#         response_body = json.loads(response['body'].read().decode('utf-8'))
#         summary = response_body['content'][0]['text']
        
#         end_time = time.time()
#         logger.info(f"Summary generation completed in {end_time - start_time:.2f} seconds")
#         logger.info(f"Generated summary length: {len(summary)} characters")
        
#         return summary
#     except Exception as e:
#         logger.error(f"Error generating summary: {str(e)}")
#         raise

# def lambda_handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
#     """Lambda function handler"""
#     overall_start_time = time.time()
#     logger.info("Lambda handler invoked")
#     logger.info(f"Event received: {json.dumps(event)}")
    
#     try:
#         # Extract the text and query from the event
#         text = event.get('text', '')
#         query = event.get('query', '')
        
#         logger.info(f"Processing request with query: '{query}'")
#         logger.info(f"Input text length: {len(text)} characters")
        
#         if not text or not query:
#             logger.error("Missing text or query parameter")
#             return {
#                 'statusCode': 400,
#                 'body': json.dumps({'error': 'Missing text or query parameter'})
#             }
        
#         # Generate embeddings for the text (optional - can be used for similarity/retrieval)
#         logger.info("Starting embedding generation process")
#         embeddings = get_embeddings(text)
#         logger.info(f"Embeddings successfully generated with dimension: {len(embeddings)}")
        
#         # Generate summary based on the query
#         logger.info("Starting summary generation process")
#         summary = generate_summary(text, query)
#         logger.info("Summary successfully generated")
        
#         overall_end_time = time.time()
#         logger.info(f"Total processing time: {overall_end_time - overall_start_time:.2f} seconds")
        
#         return {
#             'statusCode': 200,
#             'body': json.dumps({
#                 'summary': summary,
#                 'embedding_dimension': len(embeddings),
#                 'processing_time_seconds': round(overall_end_time - overall_start_time, 2)
#                 # 'embeddings': embeddings  # Commented out as embeddings can be large
#             })
#         }
#     except Exception as e:
#         logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)})
#         }




# Simplified Embedding Caching Approach

import boto3
import json
import os
import time
import logging
import hashlib
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("bedrock-summarizer")

# Initialize Bedrock client
logger.info("Initializing Bedrock client")
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.environ.get('AWS_REGION', 'us-east-1')
)
logger.info(f"Bedrock client initialized for region: {os.environ.get('AWS_REGION', 'us-east-1')}")

# Constants for models and cache
CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
TITAN_EMBEDDINGS_MODEL_ID = "amazon.titan-embed-text-v1"
CACHE_DIR = "embeddings_cache"
CACHE_FILE = os.path.join(CACHE_DIR, "embeddings_cache.pkl")

# Ensure cache directory exists
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
logger.info(f"Using cache directory: {CACHE_DIR}")
logger.info(f"Using cache file: {CACHE_FILE}")
logger.info(f"Using Claude model: {CLAUDE_MODEL_ID}")
logger.info(f"Using Embeddings model: {TITAN_EMBEDDINGS_MODEL_ID}")

# Global cache dictionary (loaded from file when needed)
embedding_cache = {}

def get_text_hash(text: str) -> str:
    """Generate a deterministic hash for the text"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def load_embedding_cache() -> Dict[str, List[float]]:
    """Load the embedding cache from file"""
    global embedding_cache
    
    if embedding_cache:
        logger.info("Using already loaded embedding cache")
        return embedding_cache
        
    if os.path.exists(CACHE_FILE):
        logger.info(f"Loading embedding cache from {CACHE_FILE}")
        try:
            with open(CACHE_FILE, 'rb') as f:
                embedding_cache = pickle.load(f)
            logger.info(f"Loaded cache with {len(embedding_cache)} entries")
            return embedding_cache
        except Exception as e:
            logger.warning(f"Failed to load embedding cache: {str(e)}")
            embedding_cache = {}
    else:
        logger.info(f"No cache file found at {CACHE_FILE}, starting with empty cache")
        embedding_cache = {}
    
    return embedding_cache

def save_embedding_cache() -> bool:
    """Save the embedding cache to file"""
    try:
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(embedding_cache, f)
        logger.info(f"Saved embedding cache with {len(embedding_cache)} entries to {CACHE_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to save embedding cache: {str(e)}")
        return False

def get_embeddings(text: str) -> tuple[List[float], bool]:
    """Generate or retrieve embeddings for the given text"""
    text_hash = get_text_hash(text)
    
    # Load cache if needed
    cache = load_embedding_cache()
    
    # Check if text hash exists in cache
    if text_hash in cache:
        logger.info(f"Found cached embeddings for text hash: {text_hash}")
        return cache[text_hash], True
    
    # If not in cache, generate new embeddings
    start_time = time.time()
    logger.info("Starting new embedding generation with Titan Embeddings model")
    
    try:
        logger.info(f"Preparing request for text of length: {len(text)} characters")
        response = bedrock.invoke_model(
            modelId=TITAN_EMBEDDINGS_MODEL_ID,
            body=json.dumps({
                "inputText": text
            })
        )
        logger.info("Received response from Titan Embeddings model")
        
        response_body = json.loads(response['body'].read().decode('utf-8'))
        embeddings = response_body['embedding']
        
        end_time = time.time()
        logger.info(f"Embedding generation completed in {end_time - start_time:.2f} seconds")
        logger.info(f"Generated embeddings with dimension: {len(embeddings)}")
        
        # Store in cache
        cache[text_hash] = embeddings
        if save_embedding_cache():
            logger.info("Embeddings successfully cached for future use")
        
        return embeddings, False
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise

def generate_summary(text: str, query: str) -> str:
    """Generate summary using Claude model"""
    start_time = time.time()
    logger.info(f"Starting summary generation with Claude model")
    logger.info(f"Query: '{query}'")
    logger.info(f"Input text length: {len(text)} characters")
    
    try:
        prompt = f"""
        I need you to summarize the following text based on this query: "{query}"
        
        Text to summarize:
        {text}
        
        Please provide a concise and relevant summary focusing on aspects related to the query.
        """
        
        logger.info("Preparing request for Claude model")
        response = bedrock.invoke_model(
            modelId=CLAUDE_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": 0,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        logger.info("Received response from Claude model")
        
        response_body = json.loads(response['body'].read().decode('utf-8'))
        summary = response_body['content'][0]['text']
        
        end_time = time.time()
        logger.info(f"Summary generation completed in {end_time - start_time:.2f} seconds")
        logger.info(f"Generated summary length: {len(summary)} characters")
        
        return summary
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise

def lambda_handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    """Lambda function handler"""
    overall_start_time = time.time()
    logger.info("Lambda handler invoked")
    logger.info(f"Event received: {json.dumps(event)}")
    
    try:
        # Extract the text and query from the event
        text = event.get('text', '')
        query = event.get('query', '')
        
        logger.info(f"Processing request with query: '{query}'")
        logger.info(f"Input text length: {len(text)} characters")
        
        if not text or not query:
            logger.error("Missing text or query parameter")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing text or query parameter'})
            }
        
        # Generate or retrieve embeddings for the text
        logger.info("Starting embedding process")
        embeddings, from_cache = get_embeddings(text)
        logger.info(f"Embeddings {'retrieved from cache' if from_cache else 'generated'} with dimension: {len(embeddings)}")
        
        # Generate summary based on the query
        logger.info("Starting summary generation process")
        summary = generate_summary(text, query)
        logger.info("Summary successfully generated")
        
        overall_end_time = time.time()
        logger.info(f"Total processing time: {overall_end_time - overall_start_time:.2f} seconds")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'summary': summary,
                'embedding_dimension': len(embeddings),
                'embedding_source': 'cache' if from_cache else 'generated',
                'processing_time_seconds': round(overall_end_time - overall_start_time, 2)
                # 'embeddings': embeddings  # Commented out as embeddings can be large
            })
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
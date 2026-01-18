"""
Storage clients for DataDistiller 2.0
Handles S3/MinIO and PostgreSQL operations
"""

from minio import Minio
from minio.error import S3Error
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from pathlib import Path
from typing import Optional, Dict, List
import io

logger = logging.getLogger(__name__)


class MinIOClient:
    """S3-compatible storage client using MinIO"""
    
    def __init__(
        self,
        endpoint: str = "localhost:9002",
        access_key: str = "minioadmin",
        secret_key: str = "minioadmin123",
        secure: bool = False
    ):
        """Initialize MinIO client"""
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = "datadistiller-docs"
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"✅ Created bucket: {self.bucket_name}")
            else:
                logger.info(f"✅ Bucket exists: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"❌ Error checking bucket: {e}")
            raise
    
    def upload_file(self, file_path: str, object_name: str) -> Dict[str, str]:
        """
        Upload file to MinIO
        
        Args:
            file_path: Local file path
            object_name: S3 object key
            
        Returns:
            Dict with bucket and key
        """
        try:
            file_size = Path(file_path).stat().st_size
            
            with open(file_path, 'rb') as file_data:
                self.client.put_object(
                    self.bucket_name,
                    object_name,
                    file_data,
                    file_size
                )
            
            logger.info(f"✅ Uploaded {file_path} to s3://{self.bucket_name}/{object_name}")
            
            return {
                'bucket': self.bucket_name,
                'key': object_name,
                'size': file_size
            }
        
        except S3Error as e:
            logger.error(f"❌ Upload failed: {e}")
            raise
    
    def upload_bytes(self, data: bytes, object_name: str, content_type: str = "application/octet-stream") -> Dict[str, str]:
        """
        Upload bytes to MinIO
        
        Args:
            data: Bytes to upload
            object_name: S3 object key
            content_type: MIME type
            
        Returns:
            Dict with bucket and key
        """
        try:
            data_stream = io.BytesIO(data)
            
            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                len(data),
                content_type=content_type
            )
            
            logger.info(f"✅ Uploaded {len(data)} bytes to s3://{self.bucket_name}/{object_name}")
            
            return {
                'bucket': self.bucket_name,
                'key': object_name,
                'size': len(data)
            }
        
        except S3Error as e:
            logger.error(f"❌ Upload failed: {e}")
            raise
    
    def download_file(self, object_name: str, file_path: str):
        """Download file from MinIO"""
        try:
            self.client.fget_object(
                self.bucket_name,
                object_name,
                file_path
            )
            logger.info(f"✅ Downloaded s3://{self.bucket_name}/{object_name} to {file_path}")
        except S3Error as e:
            logger.error(f"❌ Download failed: {e}")
            raise
    
    def download_bytes(self, object_name: str) -> bytes:
        """Download file as bytes from MinIO"""
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.info(f"✅ Downloaded {len(data)} bytes from s3://{self.bucket_name}/{object_name}")
            return data
        
        except S3Error as e:
            logger.error(f"❌ Download failed: {e}")
            raise
    
    def delete_file(self, object_name: str):
        """Delete file from MinIO"""
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"✅ Deleted s3://{self.bucket_name}/{object_name}")
        except S3Error as e:
            logger.error(f"❌ Delete failed: {e}")
            raise


class PostgresClient:
    """PostgreSQL database client for metadata and status tracking"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "datadistiller",
        user: str = "datadistiller",
        password: str = "datadistiller123"
    ):
        """Initialize PostgreSQL client"""
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self._test_connection()
    
    def _test_connection(self):
        """Test database connection"""
        try:
            conn = psycopg2.connect(**self.conn_params)
            conn.close()
            logger.info("✅ PostgreSQL connection successful")
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection failed: {e}")
            raise
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.conn_params)
    
    def create_job(self, job_data: Dict) -> str:
        """
        Create new document processing job
        
        Args:
            job_data: Job metadata
            
        Returns:
            job_id
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO document_jobs 
                    (job_id, filename, file_size, content_type, s3_bucket, s3_key, status)
                    VALUES (%(job_id)s, %(filename)s, %(file_size)s, %(content_type)s, 
                            %(s3_bucket)s, %(s3_key)s, %(status)s)
                    RETURNING job_id
                """, job_data)
                
                job_id = cur.fetchone()[0]
                conn.commit()
                
                logger.info(f"✅ Created job: {job_id}")
                return job_id
        
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Failed to create job: {e}")
            raise
        finally:
            conn.close()
    
    def update_job_status(self, job_id: str, status: str, progress: int = None, error: str = None):
        """Update job status"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                if error:
                    cur.execute("""
                        UPDATE document_jobs 
                        SET status = %s, progress = COALESCE(%s, progress), error_message = %s
                        WHERE job_id = %s
                    """, (status, progress, error, job_id))
                else:
                    cur.execute("""
                        UPDATE document_jobs 
                        SET status = %s, progress = COALESCE(%s, progress)
                        WHERE job_id = %s
                    """, (status, progress, job_id))
                
                conn.commit()
                logger.info(f"✅ Updated job {job_id}: status={status}, progress={progress}")
        
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Failed to update job: {e}")
            raise
        finally:
            conn.close()
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get job status"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT job_id, filename, file_size, status, progress, 
                           total_chunks, processed_chunks, error_message,
                           created_at, updated_at, completed_at
                    FROM document_jobs
                    WHERE job_id = %s
                """, (job_id,))
                
                result = cur.fetchone()
                return dict(result) if result else None
        
        finally:
            conn.close()
    
    def list_jobs(self, limit: int = 100, status: str = None) -> List[Dict]:
        """List recent jobs"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if status:
                    cur.execute("""
                        SELECT job_id, filename, file_size, status, progress, 
                               created_at, updated_at
                        FROM document_jobs
                        WHERE status = %s
                        ORDER BY created_at DESC
                        LIMIT %s
                    """, (status, limit))
                else:
                    cur.execute("""
                        SELECT job_id, filename, file_size, status, progress, 
                               created_at, updated_at
                        FROM document_jobs
                        ORDER BY created_at DESC
                        LIMIT %s
                    """, (limit,))
                
                results = cur.fetchall()
                return [dict(row) for row in results]
        
        finally:
            conn.close()
    
    def create_chunk(self, chunk_data: Dict) -> str:
        """Create chunk record"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO document_chunks 
                    (chunk_id, job_id, chunk_index, content, content_hash, status)
                    VALUES (%(chunk_id)s, %(job_id)s, %(chunk_index)s, 
                            %(content)s, %(content_hash)s, %(status)s)
                    RETURNING chunk_id
                """, chunk_data)
                
                chunk_id = cur.fetchone()[0]
                conn.commit()
                
                return chunk_id
        
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Failed to create chunk: {e}")
            raise
        finally:
            conn.close()
    
    def update_chunk_status(self, chunk_id: str, status: str, vector_id: str = None, error: str = None):
        """Update chunk status"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE document_chunks 
                    SET status = %s, vector_id = COALESCE(%s, vector_id), error_message = %s
                    WHERE chunk_id = %s
                """, (status, vector_id, error, chunk_id))
                
                conn.commit()
        
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Failed to update chunk: {e}")
            raise
        finally:
            conn.close()

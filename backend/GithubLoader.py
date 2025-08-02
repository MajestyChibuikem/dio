from git import Repo
from langchain_community.document_loaders import GitLoader
import os
from dotenv import load_dotenv

load_dotenv()


def file_filter(file_path):
    ignore_filepaths = ["package-lock.json"]
    # return file_path.endswith(".md")
    for ignore_filepath in ignore_filepaths:
        if ignore_filepath in file_path:
            return False
    return True


class GithubLoader:
    def __init__(self):
        """
        this class is responsible for loading in a github repository
        """

    def load(self, url: str):
        tmp_path = f"/tmp/github_repo"
        # remove the folder if it exists
        if os.path.exists(tmp_path):
            os.system(f"rm -rf {tmp_path}")
        
        # Clean the URL to get the base repository URL
        # Remove /tree/main, /tree/master, /blob/main, etc.
        import re
        clean_url = re.sub(r'/(tree|blob)/(main|master|develop|dev).*$', '', url)
        # Remove trailing slash
        clean_url = clean_url.rstrip('/')
        
        print(f"Original URL: {url}")
        print(f"Cleaned URL: {clean_url}")
        
        try:
            repo = Repo.clone_from(
                clean_url,
                to_path=tmp_path,
                depth=1,  # Shallow clone for faster download
                single_branch=True,  # Only clone the default branch
            )
        except Exception as e:
            print(f"Error cloning repository with gitpython: {e}")
            # Try with a longer timeout and different options
            import subprocess
            import shutil
            
            # Remove the failed directory
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)
            
            # Try with git command directly with timeout and different options
            try:
                print(f"Trying subprocess git clone for {clean_url}")
                result = subprocess.run([
                    'git', 'clone', '--depth', '1', '--single-branch',
                    '--quiet', clean_url, tmp_path
                ], timeout=300, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"Git clone failed with return code {result.returncode}")
                    print(f"stderr: {result.stderr}")
                    raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
                
                repo = Repo(tmp_path)
                print(f"Successfully cloned {clean_url}")
            except subprocess.TimeoutExpired:
                raise Exception(f"Git clone timed out for {clean_url}")
            except subprocess.CalledProcessError as e:
                print(f"Git clone failed with subprocess: {e}")
                # Try one more time with different options
                try:
                    if os.path.exists(tmp_path):
                        shutil.rmtree(tmp_path)
                    
                    print(f"Trying alternative git clone method for {clean_url}")
                    result = subprocess.run([
                        'git', 'clone', '--depth', '1', '--single-branch',
                        '--config', 'http.postBuffer=524288000',
                        '--config', 'http.maxRequestBuffer=100M',
                        '--config', 'core.compression=0',
                        clean_url, tmp_path
                    ], timeout=600, capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
                    
                    repo = Repo(tmp_path)
                    print(f"Successfully cloned {clean_url} with alternative method")
                except Exception as e2:
                    raise Exception(f"All git clone methods failed for {clean_url}: {e2}")
            except Exception as e:
                raise Exception(f"Failed to clone repository {clean_url}: {e}")
        branch = repo.head.reference

        loader = GitLoader(repo_path=tmp_path, branch=branch, file_filter=file_filter)
        return loader


# github_loader = GithubLoader()
# loader = github_loader.load("https://github.com/travisleow/codehub")
# docs = loader.load()
# for doc in docs:
#     print(doc.metadata["source"])

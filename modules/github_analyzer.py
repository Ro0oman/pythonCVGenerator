import requests
import json
import base64
import os

def get_recent_github_repos(github_url: str, limit: int = 3):
    """
    Fetches the [limit] most recently updated repositories and their READMEs.
    """
    github_user = github_url.rstrip('/').split('/')[-1]
    api_url = f"https://api.github.com/users/{github_user}/repos?sort=updated&direction=desc&per_page={limit}"
    
    headers = {}
    token = os.getenv("GITHUB_TOKEN")
    if token and token != "your_github_token":
        headers["Authorization"] = f"token {token}"
        
    print(f"[*] Analizando GitHub de: {github_user}")
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Error al obtener repos: {response.status_code}")
            return []
            
        repos = response.json()
        projects_data = []
        
        for repo in repos:
            repo_name = repo['name']
            readme_url = f"https://api.github.com/repos/{github_user}/{repo_name}/readme"
            
            readme_content = ""
            readme_res = requests.get(readme_url, headers=headers)
            if readme_res.status_code == 200:
                content_b64 = readme_res.json().get('content', '')
                readme_content = base64.b64decode(content_b64).decode('utf-8', errors='ignore')
            
            projects_data.append({
                "name": repo_name,
                "description": repo.get('description', ''),
                "readme_summary": readme_content[:2000],  # Shortened for LLM
                "languages": repo.get('language', 'Unknown')
            })
            
        return projects_data
        
    except Exception as e:
        print(f"[!] Error en GitHub Analyzer: {e}")
        return []

if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        data = get_recent_github_repos(sys.argv[1])
        print(json.dumps(data, indent=2))

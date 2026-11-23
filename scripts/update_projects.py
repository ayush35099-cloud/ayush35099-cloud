import os
import re
import urllib.request
import json
import subprocess

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        try:
            p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = p.communicate(input="protocol=https\nhost=github.com\n")
            for line in stdout.splitlines():
                if line.startswith("password="):
                    token = line.split("=", 1)[1].strip()
                    break
        except Exception:
            pass
    return token

def github_request(url, token=None):
    headers = {
        "User-Agent": "Antigravity-Profile-Updater",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return None

def count_personal_commits(repo_name, username="ayush35099-cloud", token=None):
    page = 1
    my_commits = 0
    
    while True:
        url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=100&page={page}"
        commits = github_request(url, token)
        if not commits or not isinstance(commits, list) or len(commits) == 0:
            break
        for c in commits:
            author_obj = c.get('author') or {}
            author_login = (author_obj.get('login') or '').lower()
            commit_data = c.get('commit', {})
            commit_author = commit_data.get('author', {})
            author_email = (commit_author.get('email') or '').lower()
            author_name = (commit_author.get('name') or '').lower()
            
            if author_login == username.lower() or 'ayush35099' in author_email or 'ayush' in author_name:
                my_commits += 1
                
        if len(commits) < 100:
            break
        page += 1
        
    return my_commits

# Registry of major candidate projects evaluated for profile showcase
MAJOR_PROJECTS_REGISTRY = {
    "BharatStore": {
        "display_name": "BharatStore (BharatKart)",
        "tagline": "Cloud-Native Enterprise E-Commerce Platform",
        "description": "An omni-channel marketplace platform connecting regional stores across India with event-driven Kafka messaging, OpenSearch catalog indexing, and real-time inventory sync.",
        "tech_stack": "Python, Flask 3.0, PostgreSQL, SQLite, Apache Kafka",
        "badges": [
            ("Python", "3776AB", "python", "white"),
            ("Flask", "000000", "flask", "white"),
            ("PostgreSQL", "316192", "postgresql", "white"),
            ("Kafka", "231F20", "apache-kafka", "white")
        ],
        "repo_url": "https://github.com/ayush35099-cloud/BharatStore",
        "demo_url": None,
        "is_major": True,
        "primary_repos": ["BharatStore"]
    },
    "Ckd-Screening-System": {
        "display_name": "RenalCare: CKD Screening System",
        "tagline": "Clinical ML Decision-Support Platform",
        "description": "An applied machine learning decision-support platform designed to assist healthcare workers in primary health centres detect early physiological markers of CKD using 24 clinical parameters.",
        "tech_stack": "Python 3.10+, Flask 3.0, Scikit-Learn 1.7, Clinical ML",
        "badges": [
            ("Python", "3776AB", "python", "white"),
            ("Flask", "000000", "flask", "white"),
            ("Scikit-Learn", "F7931E", "scikit-learn", "white"),
            ("Clinical ML", "00FF99", "python", "0D1117")
        ],
        "repo_url": "https://github.com/ayush35099-cloud/Ckd-Screening-System",
        "demo_url": None,
        "is_major": True,
        "primary_repos": ["Ckd-Screening-System"]
    },
    "Smart-Campus": {
        "display_name": "Smart Campus Attendance Portal",
        "tagline": "Student Attendance & Academic Management Portal",
        "description": "A centralized university management portal engineered to automate student attendance computation, track course threshold eligibility, issue exam alerts, and provide role-based authentication.",
        "tech_stack": "JavaScript, HTML5, CSS3, Responsive Design, Session Auth",
        "badges": [
            ("JavaScript", "F7DF1E", "javascript", "black"),
            ("HTML5", "E34F26", "html5", "white"),
            ("CSS3", "1572B6", "css3", "white")
        ],
        "repo_url": "https://github.com/ayush35099-cloud/smart_campus_final_v2",
        "demo_url": None,
        "is_major": True,
        "primary_repos": ["smart_campus_final_v2", "PYTHON_PROJECT1"]
    },
    "PredictED": {
        "display_name": "PredictED: Academic AI Dashboard",
        "tagline": "Academic Analytics & Bunk Margin Predictor",
        "description": "An intelligent academic decision dashboard engineered for university students. Features smart attendance analytics, predictive bunk calculations, automated threshold warning alerts, and an AI study companion.",
        "tech_stack": "Python, Pandas, Scikit-Learn, Modern Web UI, AI Analytics",
        "badges": [
            ("Python", "3776AB", "python", "white"),
            ("Scikit-Learn", "F7931E", "scikit-learn", "white"),
            ("AI Analytics", "00FF99", "google", "0D1117"),
            ("Academic AI", "BC8CFF", "github", "0D1117")
        ],
        "repo_url": "https://github.com/ayush35099-cloud",
        "demo_url": None,
        "is_major": True,
        "primary_repos": []
    }
}

MEDALS = ["🥇", "🥈", "🥉", "4️⃣"]

def generate_2x2_markdown(projects_ranked):
    lines = []
    lines.append('<div align="center">\n')
    lines.append('  <p><i>Featured showcase of four major development projects arranged in a 2&times;2 activity-ranked rectangular grid.</i></p>\n')
    lines.append('</div>\n\n')
    
    top4 = projects_ranked[:4]
    
    lines.append('<table width="100%">\n')
    
    # 2 rows x 2 columns = 2x2 grid
    for row_idx in range(0, len(top4), 2):
        lines.append('  <tr>\n')
        for col_idx in range(row_idx, min(row_idx + 2, len(top4))):
            p = top4[col_idx]
            rank_num = col_idx + 1
            medal = MEDALS[col_idx] if col_idx < len(MEDALS) else f"#{rank_num}"
            name = p['display_name']
            tagline = p['tagline']
            desc = p['description']
            tech = p['tech_stack']
            commits = p['commits']
            commit_str = f"{commits} Commits" if commits > 0 else "Active Flagship"
            repo_url = p['repo_url']
            badges = p['badges']
            
            badge_html = " ".join([
                f'<img src="https://img.shields.io/badge/{b[0]}-{b[1]}?style=flat-square&logo={b[2]}&logoColor={b[3]}" alt="{b[0]}" />'
                for b in badges
            ])
            
            lines.append('    <td width="50%" valign="top">\n')
            lines.append(f'      <h3 align="left">{medal} {rank_num}. <a href="{repo_url}">{name}</a></h3>\n')
            lines.append(f'      <p><b>{tagline}</b></p>\n')
            lines.append(f'      <p>{desc}</p>\n')
            lines.append(f'      <p><b>💻 Tech:</b> <code>{tech}</code></p>\n')
            lines.append(f'      <p><b>🔥 Activity:</b> <img src="https://img.shields.io/badge/My_Commits-{commit_str.replace(" ", "_")}-00FF99?style=flat-square&logo=git&logoColor=0D1117" alt="Commits" /></p>\n')
            lines.append(f'      <p>{badge_html}</p>\n')
            lines.append('      <p>\n')
            lines.append(f'        <a href="{repo_url}">\n')
            lines.append('          <img src="https://img.shields.io/badge/View_Repository-00FF99?style=for-the-badge&logo=github&logoColor=0D1117" alt="View Repository" />\n')
            lines.append('        </a>\n')
            if p.get('demo_url'):
                lines.append(f'        <a href="{p["demo_url"]}">\n')
                lines.append('          <img src="https://img.shields.io/badge/Live_Demo-BC8CFF?style=for-the-badge&logo=firefox&logoColor=0D1117" alt="Live Demo" />\n')
                lines.append('        </a>\n')
            lines.append('      </p>\n')
            lines.append('    </td>\n')
        lines.append('  </tr>\n')
        
    lines.append('</table>\n')
    return "".join(lines)

def update_readme(repo_dir=None):
    if not repo_dir:
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    readme_path = os.path.join(repo_dir, "README.md")
    token = get_token()
    username = "ayush35099-cloud"
    
    print(f"Evaluating top major projects for {username} in 2x2 grid...")
    project_scores = []
    
    for proj_id, meta in MAJOR_PROJECTS_REGISTRY.items():
        total_commits = 0
        for r in meta["primary_repos"]:
            c = count_personal_commits(r, username, token)
            print(f"  -> [{proj_id}] {r}: {c} commits")
            total_commits += c
            
        project_scores.append({
            "proj_id": proj_id,
            "display_name": meta["display_name"],
            "tagline": meta["tagline"],
            "description": meta["description"],
            "tech_stack": meta["tech_stack"],
            "badges": meta["badges"],
            "demo_url": meta.get("demo_url"),
            "commits": total_commits,
            "repo_url": meta["repo_url"]
        })
        
    # Sort strictly by commit count descending!
    project_scores.sort(key=lambda x: x["commits"], reverse=True)
    
    # Select exactly the top 4
    top_4_projects = project_scores[:4]
    
    print("\nSelected Top 4 Major Projects (2x2 Grid):")
    for rank, p in enumerate(top_4_projects, 1):
        print(f"  Rank #{rank}: {p['display_name']} ({p['commits']} commits)")
        
    new_content = generate_2x2_markdown(top_4_projects)
    
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_text = f.read()
        
    pattern = r"<!-- PROJECTS-START -->.*?<!-- PROJECTS-END -->"
    replacement = f"<!-- PROJECTS-START -->\n\n{new_content}\n<!-- PROJECTS-END -->"
    
    if "<!-- PROJECTS-START -->" in readme_text:
        updated_readme = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)
    else:
        # Fallback if markers missing
        updated_readme = readme_text.replace("## 🚀 Top 4 Major Projects – Ranked by Development Activity", f"## 🚀 Featured Projects – 2×2 Grid\n\n{replacement}")
        
    # Ensure section header is clear:
    updated_readme = re.sub(
        r"## 🚀.*Projects.*",
        "## 🚀 Featured Projects – 2×2 Activity Grid",
        updated_readme,
        count=1
    )
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
    print(f"\nSuccessfully updated {readme_path} with 2x2 grid layout!")

if __name__ == "__main__":
    update_readme()

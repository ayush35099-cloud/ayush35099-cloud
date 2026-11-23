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
    total_commits = 0
    my_commits = 0
    
    while True:
        url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=100&page={page}"
        commits = github_request(url, token)
        if not commits or not isinstance(commits, list) or len(commits) == 0:
            break
        total_commits += len(commits)
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

PROJECT_METADATA = {
    "BharatStore": {
        "display_name": "BharatStore (BharatKart)",
        "tagline": "Cloud-Native Enterprise E-Commerce & Retail Marketplace Platform",
        "description": "A cloud-native omni-channel marketplace platform connecting regional mega-stores and fulfillment hubs across India into a unified digital commerce engine. Features real-time catalog indexing, shopping cart, and order processing.",
        "tech_stack": "Python, Flask 3.0, PostgreSQL, SQLite, Apache Kafka, OpenSearch 2.x, HTML5, CSS3",
        "badges": [
            ("Python", "3776AB", "python", "white"),
            ("Flask", "000000", "flask", "white"),
            ("PostgreSQL", "316192", "postgresql", "white"),
            ("Kafka", "231F20", "apache-kafka", "white")
        ],
        "demo_url": None
    },
    "Ckd-Screening-System": {
        "display_name": "RenalCare: Chronic Kidney Disease (CKD) Screening System",
        "tagline": "Clinical ML Decision-Support Platform for Early Detection",
        "description": "An applied machine learning decision-support platform designed to assist healthcare workers in Primary Health Centres (PHCs) and community diagnostic camps detect early physiological markers of Chronic Kidney Disease (CKD) using 24 routine laboratory parameters.",
        "tech_stack": "Python 3.10+, Flask 3.0, Scikit-Learn 1.7, Machine Learning, Clinical Decision Support",
        "badges": [
            ("Python", "3776AB", "python", "white"),
            ("Flask", "000000", "flask", "white"),
            ("Scikit-Learn", "F7931E", "scikit-learn", "white"),
            ("Healthcare ML", "00FF99", "python", "0D1117")
        ],
        "demo_url": None
    },
    "PYTHON_PROJECT1": {
        "display_name": "Campus Academic Portal & Authentication Suite",
        "tagline": "Role-Based Academic Management & User Verification System",
        "description": "A modular academic role-based web application providing dedicated student and faculty portals, secure session validation, student attendance management, and administrative dashboards.",
        "tech_stack": "JavaScript, HTML5, CSS3, Session Auth",
        "badges": [
            ("JavaScript", "F7DF1E", "javascript", "black"),
            ("HTML5", "E34F26", "html5", "white"),
            ("CSS3", "1572B6", "css3", "white")
        ],
        "demo_url": None
    },
    "ToDoList": {
        "display_name": "TaskFlow: Interactive Productivity & Task Management",
        "tagline": "Modern Task Tracker & Productivity Organizer",
        "description": "A lightweight, responsive task and workflow management application designed for developers and students to schedule priorities, monitor completion status, and maintain daily momentum.",
        "tech_stack": "JavaScript, CSS3, HTML5, Local Storage",
        "badges": [
            ("JavaScript", "F7DF1E", "javascript", "black"),
            ("HTML5", "E34F26", "html5", "white"),
            ("CSS3", "1572B6", "css3", "white")
        ],
        "demo_url": None
    },
    "smart_campus_final_v2": {
        "display_name": "Smart Campus Attendance Management System",
        "tagline": "Student Attendance Calculation & Eligibility Notification Engine",
        "description": "A university management interface engineered to automate attendance calculation, track course percentage thresholds, and generate eligibility notifications for examinations.",
        "tech_stack": "JavaScript, HTML5, CSS3, Responsive Design",
        "badges": [
            ("JavaScript", "F7DF1E", "javascript", "black"),
            ("HTML5", "E34F26", "html5", "white"),
            ("CSS3", "1572B6", "css3", "white")
        ],
        "demo_url": None
    },
    "-Habit-Tracker": {
        "display_name": "Habit Tracker & Streak Analytics",
        "tagline": "Goal Setting & Daily Consistency Engine",
        "description": "An interactive routine management web application built to help users establish consistent habits, track consecutive day streaks, and visualize productivity milestones.",
        "tech_stack": "JavaScript, CSS3, HTML5",
        "badges": [
            ("JavaScript", "F7DF1E", "javascript", "black"),
            ("HTML5", "E34F26", "html5", "white"),
            ("CSS3", "1572B6", "css3", "white")
        ],
        "demo_url": None
    }
}

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

def generate_projects_markdown(projects_ranked):
    lines = []
    lines.append('<div align="center">\n')
    lines.append('  <p><i>Projects dynamically ordered by total personal development commits authored by <b>@ayush35099-cloud</b> (including feature branch merges).</i></p>\n')
    lines.append('</div>\n\n')
    
    lines.append('<table width="100%">\n')
    
    # We will lay them out in 2-column or clean rows
    for i, p in enumerate(projects_ranked):
        medal = MEDALS[i] if i < len(MEDALS) else f"#{i+1}"
        rank_num = i + 1
        name = p['display_name']
        tagline = p['tagline']
        desc = p['description']
        tech = p['tech_stack']
        commits = p['commits']
        repo_url = p['repo_url']
        badges = p['badges']
        
        badge_html = " ".join([
            f'<img src="https://img.shields.io/badge/{b[0]}-{b[1]}?style=flat-square&logo={b[2]}&logoColor={b[3]}" alt="{b[0]}" />'
            for b in badges
        ])
        
        lines.append('  <tr>\n')
        lines.append('    <td width="100%" valign="top">\n')
        lines.append(f'      <h3>{medal} {rank_num}. <a href="{repo_url}">{name}</a></h3>\n')
        lines.append(f'      <p><b>{tagline}</b></p>\n')
        lines.append(f'      <p>{desc}</p>\n')
        lines.append(f'      <p><b>💻 Tech Stack:</b> <code>{tech}</code></p>\n')
        lines.append(f'      <p><b>🔥 Personal Activity:</b> <img src="https://img.shields.io/badge/My_Commits-{commits}_Commits-00FF99?style=flat-square&logo=git&logoColor=0D1117" alt="Commits" /> &bull; <i>Rank #{rank_num} by commit volume</i></p>\n')
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
        
    lines.append('</table>\n\n')
    
    # Also add the spotlight card for PredictED (Flagship AI Academic System)
    lines.append('<table width="100%">\n')
    lines.append('  <tr>\n')
    lines.append('    <td width="100%" valign="top">\n')
    lines.append('      <h3>🌟 Flagship Academic AI System: PredictED</h3>\n')
    lines.append('      <p><b>AI-Powered Academic Intelligence & Bunk Margin Predictor Dashboard</b></p>\n')
    lines.append('      <p>An intelligent academic decision dashboard engineered for university students. Features smart attendance analytics, predictive bunk calculations, automated threshold warning notifications, timetable scheduling, and an interactive AI study companion.</p>\n')
    lines.append('      <p><b>💻 Tech Stack:</b> <code>Python, Pandas, Scikit-Learn, Modern Web UI, AI Analytics</code></p>\n')
    lines.append('      <p>\n')
    lines.append('        <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />\n')
    lines.append('        <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />\n')
    lines.append('        <img src="https://img.shields.io/badge/AI_Analytics-00FF99?style=flat-square&logo=google&logoColor=0D1117" alt="AI Analytics" />\n')
    lines.append('        <img src="https://img.shields.io/badge/Academic_Project-BC8CFF?style=flat-square&logo=github&logoColor=0D1117" alt="Academic" />\n')
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
    
    print(f"Inspecting commit counts for {username}...")
    project_counts = []
    
    for repo_name, meta in PROJECT_METADATA.items():
        count = count_personal_commits(repo_name, username, token)
        print(f"-> {repo_name}: {count} personal commits")
        project_counts.append({
            "repo_name": repo_name,
            "display_name": meta["display_name"],
            "tagline": meta["tagline"],
            "description": meta["description"],
            "tech_stack": meta["tech_stack"],
            "badges": meta["badges"],
            "demo_url": meta.get("demo_url"),
            "commits": count,
            "repo_url": f"https://github.com/{username}/{repo_name}"
        })
        
    # Sort by commit count descending!
    project_counts.sort(key=lambda x: x["commits"], reverse=True)
    
    print("\nFinal Ranked Order:")
    for rank, p in enumerate(project_counts, 1):
        print(f"{rank}. {p['display_name']} - {p['commits']} commits")
        
    new_content = generate_projects_markdown(project_counts)
    
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_text = f.read()
        
    pattern = r"<!-- PROJECTS-START -->.*?<!-- PROJECTS-END -->"
    replacement = f"<!-- PROJECTS-START -->\n\n{new_content}\n<!-- PROJECTS-END -->"
    
    if "<!-- PROJECTS-START -->" in readme_text:
        updated_readme = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)
    else:
        # If markers don't exist yet, insert around the projects section
        projects_section_header = "## 🚀 Featured Projects"
        if projects_section_header in readme_text:
            parts = readme_text.split(projects_section_header)
            # Find the next separator or section
            next_part = parts[1]
            sep_idx = next_part.find('<p align="center">\n  <img src="https://raw.githubusercontent.com/ayush35099-cloud/ayush35099-cloud/main/assets/separator.svg"')
            if sep_idx != -1:
                after_projects = next_part[sep_idx:]
            else:
                after_projects = ""
            updated_readme = parts[0] + "## 🚀 My Projects – Ranked by Development Activity\n\n" + replacement + "\n\n" + after_projects
        else:
            updated_readme = readme_text + "\n\n## 🚀 My Projects – Ranked by Development Activity\n\n" + replacement
            
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
    print(f"\nSuccessfully updated {readme_path}!")

if __name__ == "__main__":
    update_readme()

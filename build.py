import json
from pybtex.database.input import bibtex

def get_personal_data():
    name = ["Chang-Hsin", "Lee"]
    email = "jacky0970711835@gmail.com"
    github = "lee-910530"
    scholar = ""  # Your Google Scholar user ID (e.g. from ?user=XXXX in your profile URL)

    bio_text = f"""
                <p>
                    I am a Master’s student at the <a href="https://cssp.lab.nycu.edu.tw/" target="_blank">Chaotic Systems and Signal Processing Laboratory (CSSP Lab.)</a> at National Yang Ming Chiao Tung University (NYCU), Taiwan. My research focuses on generative AI and diffusion models.
                </p>
                <p>
                    <span style="font-weight: bold;">Bio:</span>
                    <br>
                    From 2020 to 2024, studied in the Department of Electrical Engineering at <a href="https://www.ee.tku.edu.tw/" target="_blank">Tamkang University (TKU)</a>, Taipei, Taiwan.
                    During this period, actively participated in multiple International Intelligent RoboSports Cup competitions and achieved commendable results.
                    <br>
                    Since 2024, a Master’s student in the Institute of Electrical and Control Engineering at <a href="https://cn.nycu.edu.tw/index.php?locale=en" target="_blank">National Yang Ming Chiao Tung University (NYCU)</a>
                    , under the supervision of <a href="https://cn.nycu.edu.tw/teachers.php?pa=getItem&teacher_id=286&locale=tw" target="_blank">Prof. Wu</a>.
                    Current research focuses on Explainable AI and Generative AI, with particular attention to their development and applications in intelligent systems.                </p>
                <p>
                    <a href="https://lee-910530.github.io/assets/pdf/hsin_cv.pdf" target="_blank" style="margin-right: 15px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{email}" style="margin-right: 15px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 15px"><i class="fab fa-github fa-lg"></i> GitHub</a>
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <p>
                    &copy; Copyright 2026 Chang-Hsin Lee. 
                    Powered by <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">m-niemeyer</a>. 
                    Design inspired by <a href="https://kashyap7x.github.io/" target="_blank">Kashyap Chitta</a>.                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Chih-Wei Tseng': 'https://scholar.google.com/citations?user=ybjfgNEAAAAJ&hl=zh-TW',
        'Chien-Wen Sun' : "https://scholar.google.com/citations?user=pp0bGY4AAAAJ&hl=en",
        'Bing-Fei Wu': 'https://scholar.google.com/citations?user=7-23WmIAAAAJ&hl=en',
        
        }


def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Kashyap Chitta',
                         add_links=True, equal_contribution=None, corresponding=None):
    links = get_author_dict() if add_links else {}
    s = ""

    equal_contributors = -1
    if equal_contribution is not None:
        equal_contributors = equal_contribution
    for idx, p in enumerate(persons):
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'):
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold;">{make_bold_name}</span>'
        if idx < equal_contributors:
            string_part_i += "*"
        if corresponding is not None and idx == corresponding - 1:
            string_part_i += "*"
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    if 'highlight' in entry.fields.keys():
        s = """<div style="background-color: #ffffd0; margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    else:
        s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""

    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""

    name, _, _ = get_personal_data()
    my_name = name[0] + " " + name[1].split()[0]
    gen_kw = {"make_bold_name": my_name}
    if "equal_contribution" in entry.fields.keys():
        gen_kw["equal_contribution"] = int(entry.fields["equal_contribution"])
    if "corresponding" in entry.fields.keys():
        gen_kw["corresponding"] = int(entry.fields["corresponding"])
    s += f"""{generate_person_html(entry.persons['author'], **gen_kw)} <br>"""
    
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Abs', 'pdf': 'Paper', 'supp': 'Supplementary', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    
    cite = "<pre><code>@" + entry.type + "{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_projects_data():
    """Return list of projects; each may have: title, description, img, link, code, etc."""
    return [
        {'title': 'Humanoid_Robot_Basketball_Shooting_Strategy', 
         'description': 'Through camera-based image acquisition and color-feature recognition, the robot perceives the positions of the ball and the basket. Area-based distance estimation and weighted force computation are then applied to determine the shooting power, enabling self-localization and successful shooting.', 
         'img': 'assets/img/projects/Humanoid_Robot_Basketball_Shooting_Strategy.png', 
         'link': 'assets/pdf/projects/Humanoid_Robot_Basketball_Shooting_Strategy.pdf'},
        {'title': 'Humanoid_Robot_Penalty_Kick_Strategy', 
         'description': "This project studies the mechanical design and operation of a first-generation FIRA large-sized humanoid robot for a penalty kick competition. Using a head-mounted camera to detect obstacles and field boundaries, the robot determines the penalty position, force, and direction, and executes the strategy accurately within a limited time.", 
         'img': 'assets/img/projects/Humanoid_Robot_Penalty_Kick_Strategy.png', 
         'link': 'assets/pdf/projects/Humanoid_Robot_Penalty_Kick_Strategy.pdf'},
    ]

def get_projects_html():
    projects = get_projects_data()
    if not projects:
        return "<p>No projects yet.</p>"
    s = ""
    for p in projects:
        s += """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
        if p.get('img'):
            s += f"""<img src="{p['img']}" class="img-fluid img-thumbnail" alt="Project">"""
        s += """</div><div class="col-sm-9">"""
        if p.get('link'):
            s += f"""<a href="{p['link']}" target="_blank">{p.get('title', '')}</a><br>"""
        else:
            s += f"""<span style="font-weight: bold;">{p.get('title', '')}</span><br>"""
        if p.get('description'):
            s += f"""{p['description']}<br>"""
        if p.get('code'):
            s += f"""<a href="{p['code']}" target="_blank">Code</a>"""
        s += """ </div> </div> </div>"""
    return s

def get_xxx_data():
    """Return list of tabs (volunteer/activities). Each: id, label, text, images (list of URLs). Use relative paths so images work both locally and on GitHub Pages."""
    base_path = "assets/img/V_EA"
    return [
        {"id": "Robot_Camp", 
         "label": "Robot Camp", 
         "text": "<ul><li>Served as a teaching assistant during the university winter break at a high school robotics camp</li><li>Assisted students with basic robot operation and introductory programming tasks</li><li>Supported hands-on activities, troubleshooting, and team-based projects</li></ul>", 
         "images": [f"{base_path}/Robot_Camp/{i}.png" for i in range(1, 4)]},

        {"id": "Water_Safety_Assoc", 
         "label": "Water Safety Assoc.", 
         "text": "<ul><li>Participated in sea and river rescue training to develop professional water safety and lifesaving skills</li><li>Served as a lifeguard during free time to help ensure public safety in aquatic environments</li><li>Assisted in maintaining water safety and preventing potential accidents in designated areas</li></ul>", 
         "images": [f"{base_path}/Water_Safety_Assoc/{i}.png" for i in range(1, 9)]},

        {"id": "Volunteer_Club", 
         "label": "Volunteer Club", 
         "text": "<ul><li>Participated in various volunteer activities, including invoice donation campaigns and beach clean-up events</li><li>Contributed to community service initiatives aimed at environmental protection and social welfare</li><li>Collaborated with team members to support and organize volunteer projects</li></ul>", 
         "images": [f"{base_path}/Volunteer_Club/{i}.png" for i in range(1, 3)]},
    ]

def get_xxx_html():
    tabs = get_xxx_data()
    if not tabs:
        return "<p>No content yet.</p>"
    tabs_json = json.dumps(tabs)
    s = f"""
    <div id="xxx-section" style="max-width: 960px; margin: 0 auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 1.5em; flex-wrap: wrap;">
            {"".join(f'<button type="button" class="xxx-tab-btn" data-tab="{t["id"]}" style="padding: 10px 24px; background: #fff; color: #000; border: 1px solid #000; border-radius: 8px; cursor: pointer; font-size: 1em;">{t["label"]}</button>' for t in tabs)}
        </div>
        <div id="xxx-text" style="min-height: 80px; padding: 1em; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 1.5em; background: #fafafa;"></div>
        <div id="xxx-carousel" style="position: relative; margin-bottom: 2em;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 12px; min-height: 400px;">
                <button type="button" id="xxx-prev" aria-label="Previous" style="background: #f0f0f0; border: 1px solid #ccc; border-radius: 8px; width: 48px; height: 48px; cursor: pointer; flex-shrink: 0; z-index: 2;">
                    <i class="fa fa-chevron-left" style="font-size: 1.5em;"></i>
                </button>
                <div style="display: flex; align-items: center; justify-content: center; gap: 12px; flex: 0 0 auto;">
                    <div id="xxx-left" style="width: 140px; height: 140px; overflow: hidden; border-radius: 8px; opacity: 0.75; filter: blur(2px); transition: all 0.3s; background: #111;"></div>
                    <div id="xxx-center" style="width: 480px; height: 360px; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: all 0.3s; background: #111;"></div>
                    <div id="xxx-right" style="width: 140px; height: 140px; overflow: hidden; border-radius: 8px; opacity: 0.75; filter: blur(2px); transition: all 0.3s; background: #111;"></div>
                </div>
                <button type="button" id="xxx-next" aria-label="Next" style="background: #f0f0f0; border: 1px solid #ccc; border-radius: 8px; width: 48px; height: 48px; cursor: pointer; flex-shrink: 0; z-index: 2;">
                    <i class="fa fa-chevron-right" style="font-size: 1.5em;"></i>
                </button>
            </div>
            <p id="xxx-counter" style="text-align: center; margin-top: 0.5em; color: #666;">1 / 0</p>
        </div>
    </div>
    <script>
    (function() {{
        var tabs = {tabs_json};
        var currentTabIndex = 0;
        var currentImages = [];
        var centerIndex = 0;

        function getIndex(i, n) {{ return n ? ((i % n) + n) % n : 0; }}

        function setSlide() {{
            var n = currentImages.length;
            var leftEl = document.getElementById('xxx-left');
            var centerEl = document.getElementById('xxx-center');
            var rightEl = document.getElementById('xxx-right');
            var counterEl = document.getElementById('xxx-counter');
            var imgStyle = 'width: 100%; height: 100%; object-fit: contain; object-position: center;';
            if (n === 0) {{
                leftEl.innerHTML = ''; centerEl.innerHTML = ''; rightEl.innerHTML = '';
                counterEl.textContent = '0 / 0';
                return;
            }}
            var leftIdx = getIndex(centerIndex - 1, n);
            var rightIdx = getIndex(centerIndex + 1, n);
            leftEl.innerHTML = '<img src="' + currentImages[leftIdx] + '" style="' + imgStyle + '">';
            centerEl.innerHTML = '<img src="' + currentImages[centerIndex] + '" style="' + imgStyle + '">';
            rightEl.innerHTML = '<img src="' + currentImages[rightIdx] + '" style="' + imgStyle + '">';
            counterEl.textContent = (centerIndex + 1) + ' / ' + n;
        }}

        function showTab(i) {{
            currentTabIndex = i;
            var tab = tabs[i];
            document.getElementById('xxx-text').innerHTML = tab.text;
            currentImages = tab.images || [];
            centerIndex = 0;
            setSlide();
            document.querySelectorAll('.xxx-tab-btn').forEach(function(btn, j) {{
                btn.style.background = j === i ? '#f0f0f0' : '#fff';
                btn.style.color = '#000';
                btn.style.border = '1px solid #000';
            }});
        }}

        document.querySelectorAll('.xxx-tab-btn').forEach(function(btn, i) {{
            btn.onclick = function() {{ showTab(i); }};
        }});

        document.getElementById('xxx-next').onclick = function() {{
            if (currentImages.length) {{ centerIndex = getIndex(centerIndex + 1, currentImages.length); setSlide(); }}
        }};
        document.getElementById('xxx-prev').onclick = function() {{
            if (currentImages.length) {{ centerIndex = getIndex(centerIndex - 1, currentImages.length); setSlide(); }}
        }};

        showTab(0);
    }})();
    </script>
    """
    return s

def get_awards_images():
    """Return list of award carousel image paths (1.png, 2.png, ...). Place images in assets/img/awards/"""
    base = "assets/img/awards"
    return [f"{base}/{i}.png" for i in range(1, 6)]  # 1.png ~ 5.png

def get_awards_html():
    images = get_awards_images()
    if not images:
        return "<p>No award images yet.</p>"
    images_json = json.dumps(images)
    n = len(images)
    s = f"""
    <div id="awards-carousel" style="position: relative; max-width: 960px; margin: 0 auto 2em;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; min-height: 400px;">
            <button type="button" id="awards-prev" aria-label="Previous" style="background: #f0f0f0; border: 1px solid #ccc; border-radius: 8px; width: 48px; height: 48px; cursor: pointer; flex-shrink: 0; z-index: 2;">
                <i class="fa fa-chevron-left" style="font-size: 1.5em;"></i>
            </button>
            <div style="display: flex; align-items: center; justify-content: center; gap: 12px; flex: 0 0 auto;">
                <div id="awards-left" class="awards-side" style="width: 140px; height: 140px; overflow: hidden; border-radius: 8px; opacity: 0.75; filter: blur(2px); transition: all 0.3s; background: #111;"></div>
                <div id="awards-center" style="width: 480px; height: 360px; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: all 0.3s; background: #111;"></div>
                <div id="awards-right" class="awards-side" style="width: 140px; height: 140px; overflow: hidden; border-radius: 8px; opacity: 0.75; filter: blur(2px); transition: all 0.3s; background: #111;"></div>
            </div>
            <button type="button" id="awards-next" aria-label="Next" style="background: #f0f0f0; border: 1px solid #ccc; border-radius: 8px; width: 48px; height: 48px; cursor: pointer; flex-shrink: 0; z-index: 2;">
                <i class="fa fa-chevron-right" style="font-size: 1.5em;"></i>
            </button>
        </div>
        <p id="awards-counter" style="text-align: center; margin-top: 0.5em; color: #666;">1 / {n}</p>
    </div>
    <script>
    (function() {{
        var images = {images_json};
        var n = images.length;
        var centerIndex = 0;

        function getIndex(i) {{ return ((i % n) + n) % n; }}

        function setSlide() {{
            var leftIdx = getIndex(centerIndex - 1);
            var rightIdx = getIndex(centerIndex + 1);
            var leftEl = document.getElementById('awards-left');
            var centerEl = document.getElementById('awards-center');
            var rightEl = document.getElementById('awards-right');
            leftEl.innerHTML = '<img src="' + images[leftIdx] + '" style="width: 100%; height: 100%; object-fit: contain; object-position: center;">';
            centerEl.innerHTML = '<img src="' + images[centerIndex] + '" style="width: 100%; height: 100%; object-fit: contain; object-position: center;">';
            rightEl.innerHTML = '<img src="' + images[rightIdx] + '" style="width: 100%; height: 100%; object-fit: contain; object-position: center;">';
            document.getElementById('awards-counter').textContent = (centerIndex + 1) + ' / ' + n;
        }}

        document.getElementById('awards-next').onclick = function() {{
            centerIndex = getIndex(centerIndex + 1);
            setSlide();
        }};
        document.getElementById('awards-prev').onclick = function() {{
            centerIndex = getIndex(centerIndex - 1);
            setSlide();
        }};

        setSlide();
    }})();
    </script>
    """
    return s

def get_index_html():
    pub = get_publications_html()
    projects = get_projects_html()
    awards = get_awards_html()
    xxx = get_xxx_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1] + ' | AI Researcher'}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>

<body>
    <div class="container">
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 1em;">
            <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-8" style="">
                {bio_text}
            </div>
            <div class="col-md-4" style="">
                <img src="assets/img/profile.png" class="img-thumbnail" alt="Profile picture">
            </div>
        </div>
        <div class="row" style="margin-top: 1em;">
            <div class="col-sm-12" style="">
                <h4>Publications</h4>
                <hr>
                {pub}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Projects</h4>
                <hr>
                {projects}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Awards</h4>
                <hr>
                {awards}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Volunteer & Extracurricular Activities</h4>
                <hr>
                {xxx}
            </div>
        </div>
        <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
            {footer}
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')
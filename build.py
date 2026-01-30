from pybtex.database.input import bibtex

def get_personal_data():
    name = ["Chang-Hsin", "Lee (Web Building)"]
    email = "jacky0970711835@gmail.com"
    github = "lee-910530"
    scholar = ""  # 請填入您的 Google Scholar 用戶 ID（例如：從 scholar 個人頁網址 ?user=XXXX 取得）

    bio_text = f"""
                <p>
                    I am a Master’s student at the <a href="http://140.113.150.201/" target="_blank">Chaotic Systems and Signal Processing Laboratory (CSSP Lab.)</a> at National Yang Ming Chiao Tung University (NYCU), Taiwan. My research focuses on generative AI and diffusion models.
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
                    <a href="https://sshouhua.github.io/assets/pdf/cwsun_cv.pdf" target="_blank" style="margin-right: 15px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{email}" style="margin-right: 15px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 15px"><i class="fab fa-github fa-lg"></i> GitHub</a>
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <p>
                    &copy; Copyright 2025 Chien-Wen Sun. 
                    Powered by <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">m-niemeyer</a>. 
                    Design inspired by <a href="https://kashyap7x.github.io/" target="_blank">Kashyap Chitta</a>.                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Chih-Wei Tseng': 'https://scholar.google.com/citations?user=ybjfgNEAAAAJ&hl=zh-TW',
        'Bing-Fei Wu': 'https://scholar.google.com/citations?user=7-23WmIAAAAJ&hl=en',
        }


def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Kashyap Chitta', 
                         add_links=True, equal_contribution=None):
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

    if 'equal_contribution' in entry.fields.keys():
        s += f"""{generate_person_html(entry.persons['author'], equal_contribution=int(entry.fields['equal_contribution']))} <br>"""
    else: 
        s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    
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
    """回傳專案列表，每項可含：title, description, img, link, code 等"""
    return [
        # 範例：{'title': '專案名稱', 'description': '簡述', 'img': 'assets/img/xxx.png', 'link': 'https://...', 'code': 'https://github.com/...'},
    ]

def get_projects_html():
    projects = get_projects_data()
    if not projects:
        return "<p>暫無專案。</p>"
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

def get_awards_data():
    """回傳獎項列表，每項可含：title, org, year, description"""
    return [
        # 範例：{'title': '獎項名稱', 'org': '主辦單位', 'year': '2024', 'description': '簡述'},
    ]

def get_awards_html():
    awards = get_awards_data()
    if not awards:
        return "<p>暫無獎項。</p>"
    s = ""
    for a in awards:
        s += """<div style="margin-bottom: 2em;">"""
        s += f"""<span style="font-weight: bold;">{a.get('title', '')}</span>"""
        parts = [a.get('org', ''), a.get('year', '')]
        parts = [x for x in parts if x]
        if parts:
            s += f""" &ndash; <span style="font-style: italic;">{', '.join(parts)}</span>"""
        s += "<br>"
        if a.get('description'):
            s += f"""{a['description']}<br>"""
        s += """</div>"""
    return s

def get_index_html():
    pub = get_publications_html()
    projects = get_projects_html()
    awards = get_awards_html()
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
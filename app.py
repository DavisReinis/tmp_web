from flask import Flask, request, redirect, render_template
from models import Entry, Data
import json
import os

app = Flask(__name__)
data = Data()

@app.route('/')
def index():
    entries = data.load_entries()
    tags = data.load_tags()
    return render_template('teatris.html', entries = entries, tags = tags)

@app.route('/birkas')
def birkas():
    tags = data.load_tags()
    return render_template('birkas.html', tags = tags)

@app.route('/submit', methods=['POST'])
def submit():
    entries = data.load_entries()
    tags = data.load_tags()

    last_entry_id = 0
    for entry in entries:
        if entry["id"] > last_entry_id:
            last_entry_id = entry["id"]

    last_tag_id = 0
    for tag in tags:
        if tag["id"] > last_tag_id:
            last_tag_id = tag["id"]

    tag_names = request.form['tags'].split(',')
    cleaned_tag_names = []

    for name in tag_names:
        name = name.strip()
        if name:
            cleaned_tag_names.append(name)

    tag_ids = []

    for name in cleaned_tag_names:
        found = False

        for tag in tags:
            if tag["name"].lower() == name.lower():
                tag_ids.append(tag["id"])
                found = True
                break

        if not found:
            last_tag_id += 1
            new_tag = {
                "id": last_tag_id,
                "name": name
            }
            tags.append(new_tag)
            tag_ids.append(last_tag_id)

    # OOP usage
    new_entry = Entry(
        entry_id=last_entry_id + 1,
        theater=request.form['theater'],
        title=request.form['title'],
        date=request.form['date'],
        tags=tag_ids,
        notes=request.form.get('notes', '')
    )

    # Save the new entry and updated tags
    entries.append(new_entry.to_dict())
    data.save_entries(entries)
    data.save_tags(tags)

    return redirect('/')

@app.route('/ierakstaforma', methods=['GET'])
def ierakstaforma():
    tags = data.load_tags()
    entries = data.load_entries()
    return render_template('ierakstaforma.html', entries = entries, tags=tags)

@app.route('/get_data', methods=['GET'])
def get_data():
    entries = data.load_entries()
    tags = data.load_tags()
    data = {"entries":entries, "tags": tags}
    return data

@app.route('/delete_entry/<int:entry_id>', methods=['GET'])
def delete_entry(entry_id):
    entries = data.load_entries()
    filtered = [e for e in entries if e['id'] != entry_id]
    data.save_entries(filtered)
    return redirect('/')

@app.route('/delete_tag/<int:tag_id>', methods=['GET'])
def delete_tag(tag_id):
    tags = data.load_tags()
    entries = data.load_entries()
    for e in entries:
      if tag_id in e["tags"]:
        error_msg = "Nevar izdzēst birku - tā tiek izmantota kādā no ierakstiem."
        back_url = '/birkas'
        return render_template('error.html', error_msg=error_msg, back_url=back_url)
    filtered = []
    for t in tags:
      if t['id'] != tag_id:
        filtered.append(t)
    data.save_tags(filtered)
    return redirect('/birkas')

@app.route('/create_tag', methods=['GET', 'POST'])
def create_tag():
    tags = data.load_tags()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()

        for t in tags:
          if t["name"] == name:
            return render_template('error.html', error_msg = "Nezdevās izveidot. Brika ar šādu nosaukumu jau eksistē.", back_url ="/create_tag")


        new_id = max([t['id'] for t in tags], default=0) + 1
        tags.append({'id': new_id, 'name': name})
        data.save_tags(tags)

        return redirect('/birkas')

    return render_template('jaunabirka.html', tags=tags)

@app.route('/table')
def table():
    tags = data.load_tags()
    entries = data.load_entries()
    return render_template("ieraksti.html", entries = entries, tags = tags)

@app.route('/search', methods=["GET"])
def search():
    keyword = request.args.get('keyword','').strip().lower()
    keyword_lower = keyword.strip().lower()
    entries = data.load_entries()
    tags = data.load_tags()

    filtered = []

    for e in entries:
      id_str = str(e["id"])
      title = e.get("title", "")
      date = e.get("date", "")
      notes = e.get("notes", "")
      theater = e.get("theater", "")

      tag_names = []
      for tag in tags:
            if tag["id"] in e["tags"]:
                tag_names.append(tag["name"])

      found = False
      for tag_name in tag_names:
          if keyword_lower in tag_name.lower():
              found = True
              break

      if (
          keyword_lower in id_str.lower()
          or keyword_lower in title.lower()
          or keyword_lower in date.lower()
          or keyword_lower in notes.lower()
          or keyword_lower in theater.lower()
          or found
      ):
          filtered.append(e)
    return render_template("ieraksti.html", entries=filtered, tags = tags)


if __name__ == '__main__':
    app.run(debug=True)


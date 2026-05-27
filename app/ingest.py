import io
import zipfile
import requests
import frontmatter
from minsearch import Index


def read_repo_data(repo_owner, repo_name):
    branches = ["main", "master"]

    for branch in branches:
        url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/{branch}"
        resp = requests.get(url)

        if resp.status_code == 200:
            break
    else:
        raise Exception("Failed to download repository. Check repo name, branch, or visibility.")

    repository_data = []

    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename
        filename_lower = filename.lower()

        if not (filename_lower.endswith(".md") or filename_lower.endswith(".mdx")):
            continue

        try:
            with zf.open(file_info) as f_in:
                content = f_in.read().decode("utf-8", errors="ignore")
                post = frontmatter.loads(content)
                data = post.to_dict()

                if "/" in filename:
                    _, clean_filename = filename.split("/", maxsplit=1)
                else:
                    clean_filename = filename

                data["filename"] = clean_filename
                repository_data.append(data)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    zf.close()
    return repository_data


def sliding_window(seq, size=2000, step=1000):
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")

    result = []

    for i in range(0, len(seq), step):
        batch = seq[i:i + size]

        if not batch:
            break

        result.append({
            "content": batch,
            "start": i
        })

        if i + size >= len(seq):
            break

    return result


def chunk_documents(docs, size=2000, step=1000):
    chunks = []

    for doc in docs:
        doc_copy = doc.copy()
        content = doc_copy.pop("content", "")

        if not content:
            continue

        doc_chunks = sliding_window(content, size=size, step=step)

        for chunk in doc_chunks:
            chunk.update(doc_copy)

        chunks.extend(doc_chunks)

    return chunks


def index_data(repo_owner, repo_name, chunk=True):
    docs = read_repo_data(repo_owner, repo_name)

    if chunk:
        docs = chunk_documents(docs, size=2000, step=1000)

    index = Index(
        text_fields=["content", "title", "description", "filename"],
        keyword_fields=[]
    )

    index.fit(docs)

    return index

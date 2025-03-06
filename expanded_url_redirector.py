import os

import requests


def check_for_redirects(root):
    try:
        url = root
        while url is not None:
            r = requests.get(url, allow_redirects=False, timeout=10)
            redirect = r.headers.get("location")
            if redirect is not None:
                url = redirect
            else:
                print(url)
                return url
    except requests.exceptions.RequestException:
        print(root)
        return root

        # except requests.exceptions.Timeout:
        #     print(root)
        #     return root
        # except requests.exceptions.ConnectionError:
        #     print(root)
        #     return root


if __name__ == "__main__":
    context_dir = "./tweet_context"
    urls_filename = "expanded_urls.txt"
    # urls_filename = 'tweets_urls.txt'
    redirect_urls = []

    with open(os.path.join(context_dir, urls_filename), "r") as f:
        for i, line in enumerate(f):
            id_url_pair = line.split("\t")
            tweet_id = int(id_url_pair[0])
            root_url = id_url_pair[1].replace("\n", "")
            redirect_urls.append(str(tweet_id) + "\t" + check_for_redirects(root_url))

    with open(os.path.join(context_dir, "final_urls.txt"), "w") as fout:
        for redirect_url in redirect_urls:
            fout.write("%s\n" % redirect_url)
        fout.close()

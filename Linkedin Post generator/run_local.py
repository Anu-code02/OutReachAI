from post_generator import generate_post
from few_shot import FewShotPosts


def main():
    fs = FewShotPosts()
    tags = fs.get_tags()
    tag = tags[0] if tags else "Job Search"

    print("Using tag:", tag)
    result = generate_post("Short", "English", tag, "Professional", "Standard paragraphs", custom_prompt=None)
    print("\nGenerated post:\n")
    print(result)


if __name__ == "__main__":
    main()

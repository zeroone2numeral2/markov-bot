import re
import json
import pathlib

import markovify


def main():
    source_dir = pathlib.Path("./source_exported_chats")

    model_sentences = []

    for file_path in source_dir.glob("*.json"):
        print(f"loading {file_path}...")
        with open(file_path, "rb") as f:
            source_data = json.load(f)

        for message in source_data["messages"]:
            if not message["text"]:
                continue

            if isinstance(message["text"], list):
                # print(message["text"])
                for item in message["text"]:
                    if isinstance(item, str):
                        text = item
            else:
                text = message["text"]

            text = text.replace("'", "").replace('"', "")

            # sentences = re.split(', |_|-|!|\+', text)
            chat_sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
            print(chat_sentences)

            for sentence in chat_sentences:
                sentence = sentence.replace(".", "")
                model_sentences.append(sentence)

    print(f"...{len(model_sentences)} sentences loaded")

    model_text = ". ".join(model_sentences)
    model = markovify.Text(model_text, well_formed=False)

    while True:
        # sentence = model.make_sentence(tries=100)
        sentence = model.make_short_sentence(600, tries=100)
        user_input = input(f"{sentence}")
        if user_input.strip():
            break


if __name__ == "__main__":
    main()

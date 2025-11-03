from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os


def generate_summary(text: str) -> str:
    # return empty string for empty input
    if text == "":
        return ""

    # validate input
    if not isinstance(text, str):
        raise ValueError(f"Input has wrong type. Should be str, was {type(text)}")

    # load model
    model_folder = "LaurentBlanc/t5-small-finetuned"
    try:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_folder)
        tokenizer = AutoTokenizer.from_pretrained(model_folder)
    except Exception as e:
        raise RuntimeError(f"Failed to load model")

    # generate summary
    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
    try:
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=128,
            num_beams=4,
            length_penalty=2.0,
            no_repeat_ngram_size=2,
            early_stopping=True,
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        raise RuntimeError("Failed to generate and decode summary.")

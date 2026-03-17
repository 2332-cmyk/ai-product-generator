import os
from openai import OpenAI
import gradio as gr

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.environ.get("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"))

# Function: Generate product descriptions
def generate_descriptions(features, tone, audience, price_range, platform, output_format="text"):
    prompt = f"""
    Create 3 high-converting product descriptions.

    Product features:
    {features}

    Target audience: {audience}
    Price range: {price_range}
    Platform: {platform}
    Tone: {tone}

    Each description should include:
    - Catchy headline
    - Short engaging paragraph
    - Bullet points (benefits, not just features)
    - Call-to-action at the end

    Make the style appropriate for the platform and audience.
    Output format: {output_format.upper()} (if HTML, use <h2>, <p>, <ul>, <li>)
    Separate each description with ===
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional e-commerce copywriter."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600
    )
    return "\n\n---\n\n".join([desc.strip() for desc in response.choices[0].message.content.strip().split("===")])

# Function: Generate title and image prompt
def generate_title_image(features, audience, tone):
    prompt = f"""
    Based on the product features: {features}, target audience: {audience}, tone: {tone}:
    1. Suggest a catchy product title
    2. Suggest an AI image prompt for this product

    Output format:
    Title: <title>
    Image Prompt: <image prompt>
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a creative marketing specialist."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Gradio UI function
def gradio_generate_product(features, tone, audience, price_range, platform, output_format):
    descriptions = generate_descriptions(features, tone, audience, price_range, platform, output_format)
    title_image = generate_title_image(features, audience, tone)
    return f"=== Title & Image Prompt ===\n{title_image}\n\n=== Descriptions ===\n{descriptions}"

# Gradio interface
iface = gr.Interface(
    fn=gradio_generate_product,
    inputs=[
        gr.Textbox(label="Product Features", placeholder="Enter product features, separated by commas"),
        gr.Dropdown(choices=["Professional", "Fun", "Luxury", "Casual"], label="Tone"),
        gr.Textbox(label="Target Audience", placeholder="e.g., students, gamers"),
        gr.Dropdown(choices=["Budget", "Mid-range", "Premium"], label="Price Range"),
        gr.Dropdown(choices=["Amazon", "Shopify", "Website"], label="Platform"),
        gr.Dropdown(choices=["text", "markdown", "html"], label="Output Format")
    ],
    outputs=gr.Textbox(label="Generated Product Content", lines=30, interactive=False),
    title="AI Product Description Generator",
    description="Enter your product details manually to generate 3 professional product descriptions, a title, and an image suggestion."
)

# Launch Gradio
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

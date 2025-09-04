# app.py — Simple BMI Calculator with Gradio
import gradio as gr

def classify_bmi(bmi):
    """Return WHO-style BMI category."""
    if bmi < 18.5:
        return "Underweight (< 18.5)"
    elif bmi < 25.0:
        return "Normal / Healthy (18.5–24.9)"
    elif bmi < 30.0:
        return "Overweight (25.0–29.9)"
    elif bmi < 35.0:
        return "Obesity class I (30.0–34.9)"
    elif bmi < 40.0:
        return "Obesity class II (35.0–39.9)"
    else:
        return "Obesity class III (≥ 40.0)"

def calculate_bmi(units, weight, height_cm, height_ft, height_in):
    """Compute BMI based on metric or imperial inputs and return explanation."""
    try:
        weight = float(weight)
    except Exception:
        return "❌ Please enter a valid number for weight."
    if weight <= 0:
        return "❌ Weight must be greater than 0."

    if units == "Metric (kg, cm)":
        try:
            hc = float(height_cm)
        except Exception:
            return "❌ Please enter a valid number for height (cm)."
        if hc <= 0:
            return "❌ Height (cm) must be greater than 0."
        height_m = hc / 100.0
        bmi = weight / (height_m ** 2)
        calc_str = f"{weight} kg ÷ ({height_m:.2f} m)² = {bmi:.3f}"
    else:
        try:
            hf = float(height_ft)
            hi = float(height_in)
        except Exception:
            return "❌ Please enter valid numbers for height (feet and inches)."
        if hf < 0 or hi < 0:
            return "❌ Height values must be non-negative."
        total_inches = hf * 12.0 + hi
        if total_inches <= 0:
            return "❌ Total height in inches must be greater than 0."
        bmi = 703.0 * weight / (total_inches ** 2)
        calc_str = f"703 × {weight} lb ÷ ({total_inches:.1f} in)² = {bmi:.3f}"

    bmi_rounded = round(bmi, 1)
    category = classify_bmi(bmi)

    explanation = (
        f"**Your BMI:** **{bmi_rounded}**\n\n"
        f"**Category:** {category}\n\n"
        "⚠️ Notes: BMI is a simple screening tool — it does **not** directly measure body fat. "
        "It may misclassify very muscular people, pregnant people, or children. "
        "Consult a healthcare professional for personalized advice.\n\n"
        f"**Calculation:** {calc_str}"
    )
    return explanation

def update_visibility(units):
    """Show only the relevant height inputs."""
    if units == "Metric (kg, cm)":
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🧮 Simple BMI Calculator")
    with gr.Row():
        unit_choice = gr.Radio(
            choices=["Metric (kg, cm)", "Imperial (lb, ft, in)"],
            value="Metric (kg, cm)",
            label="Units"
        )
        weight_input = gr.Number(label="Weight (kg or lb)", value=70)

    with gr.Row():
        height_cm_input = gr.Number(label="Height (cm) — for Metric", value=170)
        height_ft_input = gr.Number(label="Height (feet) — for Imperial", value=5, visible=False)
        height_in_input = gr.Number(label="Height (inches) — for Imperial", value=7, visible=False)

    calculate_btn = gr.Button("Calculate BMI")
    output_md = gr.Markdown("")

    # Update visibility of inputs when units change
    unit_choice.change(
        fn=update_visibility,
        inputs=unit_choice,
        outputs=[height_cm_input, height_ft_input, height_in_input]
    )

    # Calculate BMI when button clicked
    calculate_btn.click(
        fn=calculate_bmi,
        inputs=[unit_choice, weight_input, height_cm_input, height_ft_input, height_in_input],
        outputs=output_md
    )

# Hugging Face Spaces runs demo.launch() automatically
if __name__ == "__main__":
    demo.launch()

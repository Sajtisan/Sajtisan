def generate_terminal_svg(output_filename="terminal.svg"):
    # The raw matrix data. 
    # Tuple format: (Text, Indent level, Color)
    raw_lines = [
        ("SEP", 0, "#ff003c"),
        ("> SYSTEM INITIALIZATION", 0, "#ff003c"),
        ("> LOADING AI SUBSYSTEMS... [OK]", 0, "#ff003c"),
        ("> MOUNTING TELEMETRY... [OK]", 0, "#ff003c"),
        ("> USER: R_S_DAVID // STATUS: ONLINE", 0, "#ff003c"),
        ("SEP", 0, "#ff003c"),
        ("> USER_ID: Raffai Sajti Dávid", 0, "#e0e0e0"),
        ("> ALIAS: Sajtisan", 0, "#e0e0e0"),
        ("> AFFILIATION: University of Szeged (SZTE TTIK)", 0, "#e0e0e0"),
        ("SEP", 0, "#888888"),
        ("> CURRENT_DIRECTIVES:", 0, "#e0e0e0"),
        ("- Base Framework: Computer Science", 2, "#e0e0e0"),
        ("- Focus Module: Artificial Intelligence", 2, "#e0e0e0"),
        ("SEP", 0, "#888888"),
        ("> LATEST_COMMIT: ood_detection_baseline", 0, "#e0e0e0"),
        ("> RIG_SPECS: 9L Compartmentalized SFF", 0, "#e0e0e0"),
        ("SEP", 0, "#888888"),
        ("> ACTIVE_NODES // DEPLOYED:", 0, "#e0e0e0"),
        ("- SFF-Build-Checker: Zero-Knowledge hardware validation agent", 2, "#e0e0e0"),
        ("↳ ARCHITECTURE: Gemini LLM -> Hugging Face NLP -> ScraperAPI", 4, "#888888"),
        ("- OOD-Detection-Baseline: Neural network robustness", 2, "#e0e0e0"),
        ("↳ ARCHITECTURE: TF/Keras CNN -> Temp-Scaled Inference", 4, "#888888"),
        ("- Spíd: Hex-grid strategy environment", 2, "#e0e0e0"),
        ("↳ ARCHITECTURE: Vanilla JS -> Pathfinder -> AI Controller", 4, "#888888"),
        ("- AzElsoOlimpia: Client-side event portal", 2, "#e0e0e0"),
        ("↳ ARCHITECTURE: HTML5/CSS3 -> Vanilla JS Modules", 4, "#888888"),
        ("SEP", 0, "#888888"),
        ("> QUEUED_PROCESSES // WIP:", 0, "#e0e0e0"),
        ("- MarkdownStudio: Cross-platform markdown environment", 2, "#e0e0e0"),
        ("↳ ARCHITECTURE: Avalonia UI -> .NET API -> EF Core SQLite", 4, "#888888"),
        ("- Umbra-DOM: [CLASSIFIED DIRECTIVE // PAYLOAD ENCRYPTED]", 2, "#ff003c"),
        ("- Environment-CLI: [CLASSIFIED DIRECTIVE // PAYLOAD ENCRYPTED]", 2, "#ff003c"),
        ("- BootCanvas: [CLASSIFIED DIRECTIVE // PAYLOAD ENCRYPTED]", 2, "#ff003c"),
        ("SEP", 0, "#ff003c"),
    ]

    # Terminal formatting config
    box_width = 82 # Total characters wide
    ms_per_char = 15 # Slower, more deliberate typing speed
    pause_between_lines = 0.05 # Stutter between lines
    
    # SVG Canvas Configuration
    width = 850
    line_height = 22
    padding_top = 30
    padding_left = 30
    height = padding_top + (len(raw_lines) * line_height) + 60
    char_pixel_width = 8.4 # Approx pixel width of a monospace char at size 14

    # Initialize the SVG wrapper
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <rect width="{width}" height="{height}" fill="#0a0a0a" />
    <defs>\n'''

    current_time = 0.5 
    text_elements = ""

    # Build the clipping masks and layers
    for index, (text, indent, color) in enumerate(raw_lines):
        y_pos = padding_top + (index * line_height)
        
        if text == "SEP":
            # Layer 1: Separator Line (Flashes in instantly)
            sep_string = "#" * box_width
            text_elements += f'''        <text x="{padding_left}" y="{y_pos}" fill="{color}" opacity="0">{sep_string}<animate attributeName="opacity" from="0" to="1" begin="{current_time:.2f}s" dur="0.01s" fill="freeze" /></text>\n'''
            current_time += 0.05 # Quick jump for separator lines
            
        else:
            # Prevent text from overflowing the ASCII box
            max_text_len = box_width - 4 - indent
            if len(text) > max_text_len:
                text = text[:max_text_len - 3] + "..."

            # Layer 1: The Frame Borders (Flashes in instantly)
            border_spaces = "&#160;" * (box_width - 2)
            border_string = f"#{border_spaces}#"
            text_elements += f'''        <text x="{padding_left}" y="{y_pos}" fill="{color}" opacity="0">{border_string}<animate attributeName="opacity" from="0" to="1" begin="{current_time:.2f}s" dur="0.01s" fill="freeze" /></text>\n'''

            # Layer 2: The Content (Hidden by default, revealed as mask expands)
            safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
            
            # Pad the content with exactly enough invisible spaces to align it inside the borders
            content_padding = "&#160;" * (2 + indent) 
            content_string = f"{content_padding}{safe_text}"
            
            # Mask Calculations
            line_length = len(text)
            line_duration = line_length * (ms_per_char / 1000.0)
            
            # Start the mask exactly where the text begins to avoid delay
            mask_x = padding_left + ((1.5 + indent) * char_pixel_width)
            mask_width = (line_length * char_pixel_width) + 15 

            # Generate the specific clipping mask for this line
            svg_content += f'''        <clipPath id="clip_{index}">
            <rect x="{mask_x}" y="{y_pos - 15}" width="0" height="{line_height + 5}">
                <animate attributeName="width" from="0" to="{mask_width}" begin="{current_time:.2f}s" dur="{line_duration:.2f}s" fill="freeze" />
            </rect>
        </clipPath>\n'''

            text_elements += f'''        <text x="{padding_left}" y="{y_pos}" fill="{color}" clip-path="url(#clip_{index})">{content_string}</text>\n'''

            current_time += line_duration + pause_between_lines

    svg_content += "    </defs>\n\n"
    svg_content += '''    <g font-family="Consolas, 'Share Tech Mono', 'Courier New', monospace" font-size="14" font-weight="500">\n'''
    svg_content += text_elements

    # Add the blinking cursor waiting at the bottom
    cursor_y = padding_top + (len(raw_lines) * line_height) + 15
    svg_content += f'''        <text x="{padding_left}" y="{cursor_y}" fill="#ff003c" opacity="0">
            > █
            <animate attributeName="opacity" values="0;1;0" keyTimes="0;0.5;1" dur="1s" begin="{current_time:.2f}s" repeatCount="indefinite" />
        </text>
    </g>
</svg>'''

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[{output_filename}] rendered successfully.")

if __name__ == "__main__":
    generate_terminal_svg()
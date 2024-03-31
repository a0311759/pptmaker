

import uuid  # for generating a unique random string
from flask import Flask, render_template, request, jsonify
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    modified_slides = []  # List to store modified slide data
    for slide in data:
        heading = slide['heading'].replace('\xa0', ' ')  # Replace non-breaking space with regular space
        paragraph = slide['paragraph'].replace('\xa0', ' ')  # Replace non-breaking space with regular space
        # Check if paragraph is default
        if paragraph != "Editable Paragraph 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.":
            modified_slides.append({'heading': heading, 'paragraph': paragraph})  # Store modified data
    
    # Get the path to the directory where the presentation will be saved
    directory = r'E:\projects\presentation\ppt-project\static'
    
    # Create a PowerPoint presentation
    prs = Presentation()
    
    # Add slides based on modified slide data
    for i, slide_data in enumerate(modified_slides):
        if i == 0:  # Format the first slide differently
            slide_layout = prs.slide_layouts[0]  # Title Slide layout
        else:
            slide_layout = prs.slide_layouts[1]  # Title and Content layout
            
        slide = prs.slides.add_slide(slide_layout)
        
        # Set title and content for each slide
        title = slide.shapes.title
        content = slide.placeholders[1]
        title.text = slide_data['heading']
        content.text = slide_data['paragraph']
        
        # Set font size, bold, and alignment for title and content
        if i == 0:  # Large font for the first slide
            title.text_frame.paragraphs[0].font.size = Pt(56)
            title.text_frame.paragraphs[0].font.bold = True
            title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            content.text_frame.paragraphs[0].font.size = Pt(36)
        else:
            title.text_frame.paragraphs[0].font.size = Pt(32)
            title.text_frame.paragraphs[0].font.bold = True
            title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            content.text_frame.paragraphs[0].font.size = Pt(20)
            content.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER  # Center align content
    
    # Generate a unique filename based on the current time and a random string
    unique_id = uuid.uuid4().hex[:6]  # Generate a random string
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f'presentation_{current_time}_{unique_id}.pptx')
    
    # Save the presentation with the generated filename
    prs.save(filename)
    
    print(f"Presentation saved as: {filename}")  # Print the filename in the terminal
    
    # Return the filename as part of the response
    return jsonify({'filename': filename})

if __name__ == '__main__':
    app.run(debug=True)

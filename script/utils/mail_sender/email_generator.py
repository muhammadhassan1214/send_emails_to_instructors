
def generate_email(instructor_name: str, students: list, class_info: dict) -> str:
    student_rows = ""
    for student in students:
        student_rows += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{student['name']}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><a href="mailto:{student['email']}">{student['email']}</a></td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><a href="tel:{student['phone']}">{student['phone']}</a></td>
        </tr>
        """

    # The Full HTML Template
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: 0 auto;">
    
            <h2 style="color: #2c3e50;">New Student Enrollment</h2>
    
            <p><strong>Instructor {instructor_name},</strong></p>
    
            <p>A new student has signed up for your class on <strong>{class_info['date']}</strong> at <strong>{class_info['location']}</strong>.</p>
    
            <p style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #007bff;">
                It is required that you make contact with your student(s) as soon as possible to confirm attendance and provide preliminary details.
            </p>
    
            <h3>Student Contact Information</h3>
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background-color: #eee;">
                        <th style="padding: 8px;">Name</th>
                        <th style="padding: 8px;">Email</th>
                        <th style="padding: 8px;">Phone</th>
                    </tr>
                </thead>
                <tbody>
                    {student_rows}
                </tbody>
            </table>
    
            <br><br>
            <hr style="border: 0; border-top: 1px solid #eee;">
    
            <div style="font-size: 14px; color: #555;">
                <p>Many Blessings,</p>
    
                <p style="font-size: 18px; margin-bottom: 5px;"><strong>𝒩𝒶𝓉𝒽𝒶𝓃𝒾𝑒𝓁 𝒮𝒽𝑒𝓁𝓁, NREMT</strong></p>
                <p style="margin: 0;">Training Center Coordinator</p>
                <p style="margin: 2px 0;"><strong>Nashville TN Corporate Office</strong></p>
                <p style="margin: 2px 0;">640 Spence Lane, Ste 125</p>
                <p style="margin: 2px 0;">Nashville, TN 37217</p>
                <br>
                <p style="margin: 2px 0;">Office: <a href="tel:6895007044">689-500-7044</a></p>
                <p style="margin: 2px 0;">Cell: <a href="tel:3529010007">352-901-0007</a></p>
                <p style="margin: 10px 0;">Visit Us Online at <a href="https://www.codebluecprservices.com">www.codebluecprservices.com</a></p>
                <p style="margin-top: 10px;">
                    <a href="https://zoom.us/..." style="background-color: #2D8CFF; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px;">REQUEST A ZOOM MEETING With Nathaniel Shell</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

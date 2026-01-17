"""
Create Sample PDF for Testing
Generates a realistic Product Requirements Document
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path


def create_sample_prd():
    """Create a sample Product Requirements Document (PRD) as PDF"""
    
    # Output path
    output_path = Path("test_documents/sample_project_requirements.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
    # Create PDF
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2C3E50',
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#34495E',
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Content
    story.append(Paragraph("Product Requirements Document", title_style))
    story.append(Paragraph("Smart Home Automation System", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Project Overview
    story.append(Paragraph("1. Project Overview", heading_style))
    story.append(Paragraph("""
        This document outlines the requirements for developing a comprehensive Smart Home 
        Automation System that allows users to control and monitor their home devices 
        remotely through a mobile application and web dashboard.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Problem Statement
    story.append(Paragraph("2. Problem Statement", heading_style))
    story.append(Paragraph("""
        Homeowners struggle to manage multiple smart devices from different manufacturers 
        using separate apps. There is a need for a unified platform that integrates various 
        IoT devices and provides centralized control, automation, and energy monitoring.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Target Users
    story.append(Paragraph("3. Target Users", heading_style))
    story.append(Paragraph("""
        - Homeowners with smart devices (lights, thermostats, cameras, locks)<br/>
        - Property managers overseeing multiple units<br/>
        - Tech-savvy users interested in home automation<br/>
        - Energy-conscious consumers tracking usage
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Core Features
    story.append(Paragraph("4. Core Features & Requirements", heading_style))
    
    story.append(Paragraph("<b>4.1 Device Management</b>", styles['Heading3']))
    story.append(Paragraph("""
        - Add and configure smart devices (lights, locks, thermostats, cameras)<br/>
        - Support for 50+ device types from major manufacturers<br/>
        - Real-time device status monitoring<br/>
        - Group devices by room or function<br/>
        - Device health monitoring and alerts
    """, styles['BodyText']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.2 Automation & Scenes</b>", styles['Heading3']))
    story.append(Paragraph("""
        - Create custom automation rules (if-then logic)<br/>
        - Time-based scheduling (daily, weekly routines)<br/>
        - Trigger-based automation (motion, temperature, presence)<br/>
        - Pre-configured scenes (Good Morning, Away, Night, etc.)<br/>
        - Support for complex multi-device automations
    """, styles['BodyText']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.3 Remote Access</b>", styles['Heading3']))
    story.append(Paragraph("""
        - Control devices from anywhere via mobile app<br/>
        - Web dashboard for desktop access<br/>
        - Real-time notifications and alerts<br/>
        - Live camera feeds with recording<br/>
        - Voice control integration (Alexa, Google Assistant)
    """, styles['BodyText']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.4 Energy Monitoring</b>", styles['Heading3']))
    story.append(Paragraph("""
        - Track energy consumption per device<br/>
        - Historical usage analytics and graphs<br/>
        - Cost estimation based on local electricity rates<br/>
        - Energy-saving recommendations<br/>
        - Monthly and yearly consumption reports
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Technical Requirements
    story.append(Paragraph("5. Technical Requirements", heading_style))
    story.append(Paragraph("""
        <b>Platform:</b> iOS 14+, Android 10+, Web (Chrome, Safari, Firefox)<br/>
        <b>Backend:</b> Cloud-based architecture with edge computing support<br/>
        <b>Database:</b> Time-series database for sensor data, relational DB for user data<br/>
        <b>Security:</b> End-to-end encryption, OAuth 2.0, two-factor authentication<br/>
        <b>Protocols:</b> MQTT, Zigbee, Z-Wave, Wi-Fi, Bluetooth LE<br/>
        <b>Performance:</b> 
        - App load time under 2 seconds<br/>
        - Device command response under 1 second<br/>
        - Support 100 devices per home<br/>
        - 99.5% uptime SLA
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Constraints
    story.append(Paragraph("6. Constraints & Limitations", heading_style))
    story.append(Paragraph("""
        <b>Budget:</b> $150,000 development budget<br/>
        <b>Timeline:</b> 9 months from kickoff to launch<br/>
        <b>Team:</b> 2 backend developers, 2 mobile developers, 1 IoT engineer, 1 UI/UX designer<br/>
        <b>Compliance:</b> GDPR compliant, CCPA compliant for US users<br/>
        <b>Network:</b> Must work on standard home networks (no special hardware required)
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Expected Deliverables
    story.append(Paragraph("7. Expected Deliverables", heading_style))
    story.append(Paragraph("""
        - iOS mobile application<br/>
        - Android mobile application<br/>
        - Web dashboard (responsive)<br/>
        - Backend API and microservices<br/>
        - Admin panel for system management<br/>
        - User documentation and setup guides<br/>
        - API documentation for third-party integrations
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Success Metrics
    story.append(Paragraph("8. Success Metrics", heading_style))
    story.append(Paragraph("""
        - 10,000 active users within 6 months of launch<br/>
        - Average 15+ devices connected per home<br/>
        - 4.5+ star rating on app stores<br/>
        - Less than 2% crash rate<br/>
        - 70% user retention after 30 days
    """, styles['BodyText']))
    
    # Build PDF
    doc.build(story)
    
    print(f"✓ Created sample PDF: {output_path}")
    return output_path


if __name__ == '__main__':
    try:
        create_sample_prd()
    except ImportError:
        print("❌ reportlab not installed. Installing...")
        import subprocess
        subprocess.run(["pip", "install", "reportlab"], check=True)
        print("✓ reportlab installed. Run the script again.")

import requests
from typing import Dict

class JobDescriptionGenerator:
    """Generates detailed job descriptions from job titles"""
    
    # Pre-defined comprehensive job descriptions for common roles
    JOB_TEMPLATES = {
        "full stack developer": """
        Full Stack Developer - Job Description
        
        We are seeking a talented Full Stack Developer to join our dynamic team.
        
        Required Skills:
        - Frontend: React.js, Angular, Vue.js, HTML5, CSS3, JavaScript, TypeScript, Redux, Next.js
        - Backend: Node.js, Python, FastAPI, Django, Flask, Express.js, REST APIs, GraphQL
        - Database: MongoDB, PostgreSQL, MySQL, Redis, Firebase
        - DevOps: Docker, Kubernetes, CI/CD, Jenkins, GitHub Actions, AWS, Azure, GCP
        - Version Control: Git, GitHub, GitLab, Bitbucket
        - Testing: Jest, Pytest, Mocha, Selenium, Cypress
        - Other: Agile methodologies, Microservices, WebSockets, Authentication (JWT, OAuth)
        
        Responsibilities:
        - Design and develop scalable web applications
        - Build responsive user interfaces
        - Create and maintain RESTful APIs
        - Implement database schemas and optimize queries
        - Write clean, maintainable, and well-documented code
        - Collaborate with cross-functional teams
        - Participate in code reviews and technical discussions
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 2+ years of experience in full-stack development
        - Strong problem-solving skills
        - Excellent communication and teamwork abilities
        """,
        
        "data scientist": """
        Data Scientist - Job Description
        
        We are looking for an experienced Data Scientist to extract insights from large datasets.
        
        Required Skills:
        - Programming: Python, R, SQL, Scala, Java
        - Machine Learning: Scikit-learn, TensorFlow, PyTorch, Keras, XGBoost, LightGBM
        - Data Analysis: Pandas, NumPy, SciPy, Statsmodels
        - Visualization: Matplotlib, Seaborn, Plotly, Tableau, Power BI
        - Big Data: Hadoop, Spark, Hive, Kafka
        - Deep Learning: Neural Networks, CNN, RNN, LSTM, Transformers, NLP
        - Statistics: Hypothesis testing, A/B testing, Regression, Time series analysis
        - Cloud: AWS SageMaker, Azure ML, Google Cloud AI Platform
        - MLOps: MLflow, Kubeflow, Model deployment and monitoring
        
        Responsibilities:
        - Develop and deploy machine learning models
        - Analyze complex datasets to identify trends and patterns
        - Build predictive models and recommendation systems
        - Create data visualizations and dashboards
        - Collaborate with engineering teams to implement solutions
        - Communicate findings to stakeholders
        
        Qualifications:
        - Master's or PhD in Data Science, Statistics, Computer Science, or related field
        - 3+ years of experience in data science or machine learning
        - Strong mathematical and statistical foundation
        - Experience with real-world ML model deployment
        """,
        
        "software engineer": """
        Software Engineer - Job Description
        
        We are hiring a Software Engineer to build high-quality software solutions.
        
        Required Skills:
        - Programming Languages: Python, Java, C++, JavaScript, Go, Rust, C#
        - Web Development: React, Angular, Node.js, Spring Boot, .NET
        - Databases: SQL, NoSQL, PostgreSQL, MongoDB, Redis
        - System Design: Microservices, Design patterns, Scalability, Load balancing
        - Cloud Platforms: AWS, Azure, Google Cloud Platform
        - DevOps: Docker, Kubernetes, CI/CD pipelines, Terraform
        - Version Control: Git, GitHub, GitLab
        - Testing: Unit testing, Integration testing, TDD
        - Algorithms & Data Structures: Strong foundation required
        
        Responsibilities:
        - Design, develop, and maintain software applications
        - Write efficient, reusable, and reliable code
        - Troubleshoot and debug applications
        - Participate in system architecture decisions
        - Conduct code reviews and mentor junior developers
        - Optimize application performance
        - Stay updated with emerging technologies
        
        Qualifications:
        - Bachelor's or Master's in Computer Science or related field
        - 2+ years of professional software development experience
        - Strong analytical and problem-solving skills
        - Excellent collaboration and communication skills
        """,
        
        "devops engineer": """
        DevOps Engineer - Job Description
        
        We need a skilled DevOps Engineer to streamline our development and deployment processes.
        
        Required Skills:
        - Cloud Platforms: AWS, Azure, Google Cloud Platform, DigitalOcean
        - Containerization: Docker, Kubernetes, OpenShift, Container orchestration
        - CI/CD: Jenkins, GitLab CI, GitHub Actions, CircleCI, Travis CI
        - Infrastructure as Code: Terraform, CloudFormation, Ansible, Puppet, Chef
        - Scripting: Bash, Python, PowerShell, Groovy
        - Monitoring: Prometheus, Grafana, ELK Stack, Datadog, New Relic
        - Version Control: Git, GitOps practices
        - Networking: Load balancers, VPN, DNS, Firewalls
        - Security: SSL/TLS, Secrets management, Vulnerability scanning
        - Databases: MySQL, PostgreSQL, MongoDB, Redis
        
        Responsibilities:
        - Build and maintain CI/CD pipelines
        - Automate infrastructure provisioning and management
        - Monitor system performance and reliability
        - Implement security best practices
        - Optimize cloud resource utilization
        - Troubleshoot production issues
        - Collaborate with development teams
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 3+ years of DevOps experience
        - Strong Linux/Unix administration skills
        - Experience with high-availability systems
        """,
        
        "frontend developer": """
        Frontend Developer - Job Description
        
        We are seeking a creative Frontend Developer to build beautiful user interfaces.
        
        Required Skills:
        - Core: HTML5, CSS3, JavaScript, TypeScript
        - Frameworks: React.js, Next.js, Vue.js, Angular, Svelte
        - State Management: Redux, MobX, Zustand, Recoil, Context API
        - Styling: Tailwind CSS, Styled-components, SASS, LESS, Material-UI, Ant Design
        - Build Tools: Webpack, Vite, Rollup, Babel, npm, yarn, pnpm
        - Testing: Jest, React Testing Library, Cypress, Playwright
        - Performance: Web Vitals, Lighthouse, Code splitting, Lazy loading
        - Responsive Design: Mobile-first, Cross-browser compatibility
        - APIs: REST, GraphQL, WebSockets
        - Version Control: Git, GitHub
        
        Responsibilities:
        - Develop responsive and interactive web applications
        - Implement pixel-perfect designs
        - Optimize applications for maximum speed
        - Ensure cross-browser compatibility
        - Collaborate with UX/UI designers
        - Write clean and maintainable code
        - Participate in code reviews
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 2+ years of frontend development experience
        - Strong portfolio of web projects
        - Eye for design and user experience
        """,
        
        "backend developer": """
        Backend Developer - Job Description
        
        We are looking for a Backend Developer to build robust server-side applications.
        
        Required Skills:
        - Programming: Python, Java, Node.js, Go, C#, PHP, Ruby
        - Frameworks: FastAPI, Django, Flask, Spring Boot, Express.js, .NET Core
        - Databases: PostgreSQL, MySQL, MongoDB, Redis, Cassandra, DynamoDB
        - APIs: REST, GraphQL, gRPC, WebSockets
        - Authentication: JWT, OAuth2, SAML, API Keys
        - Message Queues: RabbitMQ, Kafka, Redis Queue, AWS SQS
        - Caching: Redis, Memcached, CDN
        - Cloud: AWS, Azure, Google Cloud Platform
        - Security: SQL injection prevention, XSS, CSRF, Encryption
        - Testing: Unit tests, Integration tests, API testing
        
        Responsibilities:
        - Design and develop scalable backend systems
        - Create and maintain RESTful APIs
        - Implement database schemas and optimize queries
        - Ensure application security and data protection
        - Integrate third-party services and APIs
        - Write comprehensive tests
        - Optimize server performance
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 2+ years of backend development experience
        - Strong understanding of algorithms and data structures
        - Experience with microservices architecture
        """,
        
        "machine learning engineer": """
        Machine Learning Engineer - Job Description
        
        We are hiring a Machine Learning Engineer to build and deploy ML models at scale.
        
        Required Skills:
        - Programming: Python, Java, Scala, C++
        - ML Frameworks: TensorFlow, PyTorch, Scikit-learn, Keras, JAX
        - Deep Learning: Neural Networks, CNN, RNN, LSTM, Transformers, GANs
        - NLP: BERT, GPT, Spacy, NLTK, Hugging Face Transformers
        - Computer Vision: OpenCV, YOLO, ResNet, Image processing
        - MLOps: MLflow, Kubeflow, Model versioning, A/B testing
        - Cloud ML: AWS SageMaker, Azure ML, Google AI Platform, Vertex AI
        - Big Data: Spark, Hadoop, Distributed computing
        - Deployment: Docker, Kubernetes, FastAPI, Flask, Model serving
        - Tools: Jupyter, Git, DVC, Weights & Biases
        
        Responsibilities:
        - Design and implement machine learning models
        - Build end-to-end ML pipelines
        - Deploy models to production environments
        - Monitor and improve model performance
        - Optimize models for speed and accuracy
        - Collaborate with data scientists and engineers
        - Research and implement new ML techniques
        
        Qualifications:
        - Master's or PhD in Computer Science, Machine Learning, or related field
        - 3+ years of ML engineering experience
        - Strong foundation in mathematics and statistics
        - Production ML experience required
        """,
        
        "ui ux designer": """
        UI/UX Designer - Job Description
        
        We are seeking a talented UI/UX Designer to create exceptional user experiences.
        
        Required Skills:
        - Design Tools: Figma, Adobe XD, Sketch, InVision, Adobe Creative Suite
        - Prototyping: Figma, Framer, Principle, ProtoPie
        - User Research: User interviews, Surveys, Usability testing, A/B testing
        - Wireframing: Low and high-fidelity wireframes, User flows
        - Visual Design: Typography, Color theory, Layout, Iconography
        - Interaction Design: Animations, Micro-interactions, Transitions
        - Design Systems: Component libraries, Style guides, Design tokens
        - Frontend Basics: HTML, CSS, Understanding of responsive design
        - Collaboration: Slack, Notion, Miro, Jira
        - Accessibility: WCAG guidelines, Inclusive design
        
        Responsibilities:
        - Create user-centered designs for web and mobile applications
        - Conduct user research and usability testing
        - Develop wireframes, prototypes, and mockups
        - Design intuitive user interfaces
        - Create and maintain design systems
        - Collaborate with developers and product managers
        - Present design concepts to stakeholders
        
        Qualifications:
        - Bachelor's degree in Design, HCI, or related field
        - 2+ years of UI/UX design experience
        - Strong portfolio demonstrating design process
        - Excellent communication and presentation skills
        """,
        
        "cloud engineer": """
        Cloud Engineer - Job Description
        
        We are looking for a Cloud Engineer to architect and manage cloud infrastructure.
        
        Required Skills:
        - Cloud Platforms: AWS, Azure, Google Cloud Platform, Multi-cloud
        - Compute: EC2, Lambda, Azure VMs, Google Compute Engine, Serverless
        - Storage: S3, EBS, Azure Blob Storage, Google Cloud Storage
        - Networking: VPC, Load Balancers, CloudFront, CDN, VPN
        - Databases: RDS, DynamoDB, Cosmos DB, Cloud SQL
        - Security: IAM, Security Groups, Encryption, Compliance
        - Infrastructure as Code: Terraform, CloudFormation, ARM Templates
        - Containers: Docker, Kubernetes, ECS, AKS, GKE
        - Monitoring: CloudWatch, Azure Monitor, Stackdriver, Prometheus
        - Cost Optimization: Resource tagging, Right-sizing, Reserved instances
        
        Responsibilities:
        - Design and implement cloud architecture
        - Migrate applications to cloud platforms
        - Optimize cloud costs and performance
        - Implement security best practices
        - Automate infrastructure provisioning
        - Monitor and troubleshoot cloud services
        - Provide technical guidance to teams
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 3+ years of cloud engineering experience
        - Cloud certifications (AWS, Azure, or GCP) preferred
        - Strong understanding of networking and security
        """,
        
        "mobile developer": """
        Mobile Developer - Job Description
        
        We are hiring a Mobile Developer to build native and cross-platform mobile applications.
        
        Required Skills:
        - iOS: Swift, SwiftUI, UIKit, Xcode, CocoaPods, TestFlight
        - Android: Kotlin, Java, Jetpack Compose, Android Studio, Gradle
        - Cross-platform: React Native, Flutter, Ionic, Xamarin
        - State Management: Redux, MobX, Provider, Riverpod, BLoC
        - APIs: REST, GraphQL, WebSockets
        - Local Storage: SQLite, Realm, Core Data, SharedPreferences
        - Push Notifications: FCM, APNs, OneSignal
        - Maps & Location: Google Maps, MapKit, Geolocation
        - Testing: XCTest, Espresso, Jest, Detox
        - App Store: Publishing to Apple App Store and Google Play Store
        
        Responsibilities:
        - Develop mobile applications for iOS and/or Android
        - Implement responsive and intuitive UI
        - Integrate with backend APIs and services
        - Optimize app performance and battery usage
        - Implement offline functionality
        - Debug and fix issues
        - Publish apps to app stores
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 2+ years of mobile development experience
        - Published apps in App Store or Play Store
        - Strong understanding of mobile UI/UX principles
        """
    }
    
    def generate_job_description(self, job_title: str) -> str:
        """
        Generate or fetch job description based on job title
        
        Args:
            job_title: Job title (e.g., "Full Stack Developer")
            
        Returns:
            Detailed job description
        """
        # Normalize job title
        job_title_lower = job_title.lower().strip()
        
        # Check for exact or partial matches
        for key, description in self.JOB_TEMPLATES.items():
            if key in job_title_lower or job_title_lower in key:
                return description
        
        # If no match found, generate a generic description
        return self._generate_generic_description(job_title)
    
    def _generate_generic_description(self, job_title: str) -> str:
        """Generate a generic job description for unknown roles"""
        return f"""
        {job_title} - Job Description
        
        We are seeking a talented {job_title} to join our team.
        
        Required Skills:
        - Strong technical skills relevant to {job_title}
        - Programming languages: Python, JavaScript, Java
        - Version Control: Git, GitHub
        - Problem-solving and analytical abilities
        - Communication and teamwork skills
        - Agile/Scrum methodologies
        - Cloud platforms (AWS, Azure, GCP)
        - Database management (SQL, NoSQL)
        - API development and integration
        - Testing and debugging
        
        Responsibilities:
        - Develop and maintain software applications
        - Collaborate with cross-functional teams
        - Write clean and efficient code
        - Participate in code reviews
        - Troubleshoot and resolve technical issues
        - Stay updated with industry trends
        - Contribute to technical documentation
        
        Qualifications:
        - Bachelor's degree in Computer Science or related field
        - 2+ years of relevant experience
        - Strong problem-solving skills
        - Excellent communication abilities
        """
    
    def get_available_roles(self) -> list:
        """Return list of available job templates"""
        return list(self.JOB_TEMPLATES.keys())
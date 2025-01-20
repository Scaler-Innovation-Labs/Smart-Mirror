### **Interactive Smart Mirror**

***

**Product Summary**The Smart Mirror is an AI-powered interactive device equipped with a camera and a Raspberry Pi (rPi). It provides personalized style suggestions, makeup tips, and compliments based on real-time visual analysis of the user. The mirror serves as an intelligent assistant for fashion and self-care, aiming to enhance user confidence and offer an engaging, practical experience.

**Objective**To create an user-friendly smart mirror that enhances the user's daily self-care routine by offering guidance and compliments, focusing on features like outfit suggestions, makeup recommendations, and personalized conversation.

**Project Details:** Smart Mirror is a project under Innovation Lab. Eligibility criteria to apply is having above 8 CGR, three students will be selected and put in a team to build this project. Students who are selected for it, can either:

1. Earn additional credits for this project work, which could be replaced for up to three months of internship requirement OR Get exemption for one term development course, and earn their credits through this project 

2. Fill this for to apply for this project: <https://forms.gle/NQnRrjPWHaRjb66N6>

***


### **1. Key Features**

#### **1.1 Interactive Camera & Display**

- **Camera integration**: High-definition camera embedded within the mirror for facial and outfit detection.

- **Real-time analysis**: Uses computer vision algorithms to detect facial features, outfit patterns, and colors.

- **Raspberry Pi**: Acts as the main processing unit, handling image processing, data handling, and user interactions.


#### **1.2 Style and Makeup Suggestions**

- **Outfit suggestions**: Based on weather, occasion, and the user's wardrobe (if integrated with an app).

- **Makeup tips**: Identifies user’s skin tone and suggests makeup ideas to complement their look.

- **Compliment feature**: Provides real-time, personalized compliments to boost user confidence.


#### **1.3 Conversational AI**

- **Voice recognition**: Allows for hands-free interaction, recognizing and responding to user commands.

- **Natural language processing (NLP)**: Uses AI to converse naturally, offering insights or responding to questions.

- **Personalized interactions**: Tailors responses based on prior interactions or user preferences.

- **Offline Processing:** Users would want their visual data to be processed offline, AI models using images from cameras need to run locally ensuring comfort of privacy.

***


### **2. Technical Specifications**

#### **2.1 Hardware**

- **Display**: High-resolution mirror display capable of overlaying information and recommendations without the need for touch interaction.

- **Camera**: HD or better, with wide-angle capabilities to capture full body shots.

- **Processor**: Raspberry Pi 4 with at least 4GB RAM for efficient processing.

- **Microphone and speakers**: For voice interactions and feedback.


#### **2.2 Software**

- **Operating System**: Raspberry Pi OS or similar Linux-based OS.

- **Computer Vision Library**: OpenCV or similar library for facial and clothing recognition.

- **Machine Learning Models**: Local Pre-trained models for recognizing facial features, makeup styles, and outfits.

- **Speech Recognition**: Google Speech-to-Text API or an offline solution for voice recognition.

- **NLP Engine**: GPT-based model or similar to handle conversational interactions and personality.


#### **2.3 Connectivity**

- **Wi-Fi and Bluetooth**: To connect with the internet and pair with user devices (smartphone, smartwatch, etc.).

- **Cloud Integration (Optional)**: To update style trends and AI models, as well as sync user preferences.

***


### **3. Functional Requirements**

#### **3.1 User Interface (UI)**

- **Mirror Display**: Must appear as a regular mirror when idle but overlay content on interaction.

- **Gesture Control**: Allows users to interact without physical touch, using hand movements for navigation if required.

- **Personalized Greeting**: Recognizes repeat users and greets them by name.


#### **3.2 Data Privacy and Security**

- **Privacy Mode**: Offers options to turn off the camera or disable audio processing. There needs to be fully offline mode as well, for users who want full offline 

- **Local Processing**: All image data is processed locally on the Raspberry Pi unless cloud services are required.

- **Data Storage**: Minimal data is stored unless required for personalized recommendations. User permissions for data use are mandatory.


#### **3.3 Adaptable Suggestions**

- **Wardrobe and Style Sync**: Option to sync with a mobile app where the user logs their wardrobe items.

- **Weather-based Suggestions**: Uses weather data to suggest appropriate outfits.

- **Occasion-based Suggestions**: If provided by the user, the mirror offers outfit or makeup suggestions tailored to specific events.


#### **3.4 Software Updates and Maintenance**

- **Over-the-Air (OTA) Updates**: Allows for seamless software updates.

- **Error Logs and Diagnostics**: For troubleshooting and performance improvement.

***


### **4. User Experience (UX) Considerations**

#### **4.1 Ease of Use**

- **Minimal Setup**: Should be easy for users to install and set up.

- **Voice Commands**: Enables hands-free operation, making it convenient to use while dressing.


#### **4.2 Inclusivity**

- **Diverse Beauty Standards**: Offers makeup and fashion advice that is sensitive to different skin tones, body types, and personal styles.

- **Accessibility**: Ensures that users with disabilities (e.g., low vision) can interact with the mirror using voice commands and large display text.


#### **4.3 Feedback and Customization**

- **User Feedback Loop**: Allows users to rate suggestions and compliments for better personalization over time.

- **Customizable Preferences**: Users can opt-in or out of certain features (e.g., receiving compliments or makeup tips).

***


### **5. Performance Requirements**

#### **5.1 Response Time**

- **Real-Time Analysis**: Mirror should respond within 1-2 seconds for smooth interaction.

- **Low Latency**: Fast processing of images and voice inputs for a seamless user experience.


#### **5.2 Battery and Power**

- **Energy Efficient**: Should go into standby mode when not in use to conserve power.

- **Backup Battery (Optional)**: For potential portability or backup during power outages.

***


### **6. Additional Considerations**

#### **6.1 Market Research and Competition**

- Research existing products in the smart mirror space to identify unique selling points (e.g., fashion recommendations, personalization).


#### **6.2 Scalability and Future Expansion**

- **Integration with Wearables**: Potential to sync with wearables for health data (e.g., sleep quality, steps) to recommend wellness insights.

- **Fashion and Beauty Partnerships**: Partner with brands for personalized product suggestions and ads based on user preferences.


#### **6.3 Limitations and Risks**

- **Camera Usage Concerns**: Privacy concerns regarding constant camera usage.

- **AI Limitations**: Limitations in NLP and computer vision accuracy, particularly in complex scenarios (e.g., outfit color misinterpretation).

***


### **7. Key Success Metrics**

- **User Engagement**: Average daily interactions per user.

- **Customer Satisfaction**: High ratings on suggestions, compliments, and style recommendations.

- **Privacy Compliance**: Low complaint rates regarding privacy or misuse of data.

***

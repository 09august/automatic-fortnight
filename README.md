# Study Plan Analyzer

**Note: This tool is designed specifically for Norwegian study plans at NTNU. It will not work for studyplans with different language.**

The Study Plan Analyzer is a project designed to analyze study plans, offering course advice to users. Leveraging web scraping, data analysis, and OpenAI's embeddings, it provides similarity between user-entered keywords and course information. The tool is compatible with various study programs at NTNU.

## How to Run

1. **Install Dependencies:** Ensure you have the necessary Python packages by running the command `pip install -r requirements.txt`.
2. **Obtain OpenAI API Key:** Insert your OpenAI API key into the designated field in `main.py`.
3. **Download NTNU Study Plan:** Download the study plan PDF from your NTNU study site, and place the file in the same folder as the repository
4. **Run the Application:** Execute `main.py` to initiate the Study Plan Analyzer.

   

## Usage

The Study Plan Analyzer can be interacted with through the following commands:

- `help`: Provides information about other commands.
- `courses`: Plots each course to similarity and profile.
  
<img src="https://drive.google.com/uc?id=1eu3sKpNJLPMkPUZ2Wl1zmV-6SGHmqNVQ" height="240" width="750" >  <img src="https://drive.google.com/uc?id=1HfXneD7TuU2daB_cXVQ_nIwARFfZKTsV" height="240" width="750" >


- `profile`: Generates a bar plot of each profile based on maximum possible similarity.
<img src="https://drive.google.com/uc?id=1GBVoxM8Pwa6-M7lS1KCmtpZYruMj9AyP" height="240" width="600" >

- `advice`: Returns advised courses per semester based on user-provided keywords.
<img src="https://drive.google.com/uc?id=1WwatIReQ69zDC0lNML7-NYr5RHjm1KDb" height="240" width="1000" >


Keywords used in these cases were: 

For 'Biotechnology and chemistry' `courses` command:   "Biologi,Genteknologi,CRISPR,Proteinsyntese,Enzymer"



For 'Engineering and ICT' `profile` command: "Design,Materialer,Termodynamikk,Automatisering,Robotikk,Toleranser" 

## Contribution

While this project is a hobby, contributions are welcomed. If you believe your changes could benefit others, please open a pull request to merge your changes into the main branch. Ensure your code is well-documented.

## License
```plaintext
MIT License

Copyright (c) [2023] [August Myhre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

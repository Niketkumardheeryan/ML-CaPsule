import streamlit as st


def main():
    """welcome page"""
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to PulseLang Web App! 👋")

    st.sidebar.success("Select a web page above ☝️")

    st.markdown(
        """
        The PulseLang is a Streamlit web application designed for translating between various dialects. 
        The issue of language differences has long hindered effective communication. Over the years, 
        difficulties in information exchange between countries have been prevalent. Traditionally, 
        language interpreters need to be fluent in both the source and target languages. 
        However, this method has proven neither productive nor favorable. Moreover, learning different 
        languages can be challenging due to language barriers. Hiring a tutor incurs additional expenses 
        and may not be the most efficient or effective method.
     
    
        To address these issues, the study developed an web app language converter app aimed at simplifying 
        language learning and facilitating stress-free communication. The web application supports translation 
        between the most widely spoken languages globally, including English, Spanish, Arabic, Hindi, French, and Chinese. 
        This application can be particularly useful for tourists, enabling them to communicate effectively, integrate with 
        local communities, and access accurate information.
        
        ### Want to know about project's gitHub repository?
        - Check out [PulseLang](https://github.com/pulselang)
    
    """
    )
    st.snow()


if __name__ == "__main__":
    main()

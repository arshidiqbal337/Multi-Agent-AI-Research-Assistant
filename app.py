import streamlit as st
from agents import run_pipeline,load_demo

st.set_page_config(page_title='Multi-Agent Research Assistant',page_icon='📚',layout='wide')
st.title('📚 Multi-Agent AI Research Assistant')
st.caption('Offline, evidence-grounded prototype | Search → Summarize → Verify → Report')
st.info('This is a transparent extractive multi-agent prototype, not an LLM-powered literature search engine. It does not browse the web or independently fact-check claims.')
with st.sidebar:
    st.header('Research documents')
    files=st.file_uploader('Upload .txt research notes or paper text',type=['txt'],accept_multiple_files=True)
    use_demo=st.checkbox('Include demo research notes',value=True)
    st.markdown('**Agents:** Search · Summary · Evidence Check · Report')
docs=load_demo() if use_demo else {}
for f in files or []:
    try:
        docs[f.name]=f.getvalue().decode('utf-8')
    except UnicodeDecodeError:
        st.warning(f'{f.name}: please upload UTF-8 text.')
question=st.text_input('Research question','How does retrieval-augmented generation reduce hallucinations?')
if st.button('Run research agents',type='primary'):
    if not question.strip():
        st.error('Please enter a research question.')
    elif not docs:
        st.error('Upload a .txt file or enable demo notes.')
    else:
        result=run_pipeline(question,docs)
        a,b=st.columns(2)
        with a:
            st.subheader('🔎 Search Agent')
            st.write(f"Found {len(result['evidence'])} matching passages")
            for item in result['evidence']:
                st.markdown(f"**{item['source']}** · score {item['score']:.2f}")
                st.write(item['sentence'])
        with b:
            st.subheader('📝 Summary Agent')
            st.write(result['summary'])
            st.subheader('🛡️ Verification Agent')
            st.write(result['verification']['status'])
            st.caption(result['verification']['note'])
        st.subheader('📄 Report Agent')
        st.markdown(result['report'])
        st.download_button('Download Markdown report',result['report'],file_name='research_report.md',mime='text/markdown')

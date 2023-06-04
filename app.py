import streamlit as st
from pytube import YouTube
import re
from pathlib import Path
import tempfile
import uuid 

downloads_path = str(Path.home() / "Downloads")
print(downloads_path)




st.set_page_config(page_title="YTAna ", page_icon="💙", layout="wide", )     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1495839760557-d150d64b4469?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

@st.cache_data
def make_tempdir() -> Path:
    '''Make temp dir for each user session and return path to it
    '''
    if 'tempfiledir' not in st.session_state:
        tempfiledir = Path(tempfile.gettempdir())
        tempfiledir = tempfiledir.joinpath(f"streamlit_{uuid.uuid4()}")   # make unique subdir
        tempfiledir.mkdir(parents=True, exist_ok=True)  # make dir if not exists
        st.session_state['tempfiledir'] = tempfiledir
    return st.session_state['tempfiledir']


@st.cache_resource()#allow_output_mutation=True)
def get_info(url):
    yt = YouTube(url)
    streams= yt.streams.filter(progressive= True, type= 'video')
    details= {}
    details["image"]= yt.thumbnail_url
    details["streams"]= streams
    details["title"]= yt.title
    details["length"]= yt.length
    itag, resolutions, vformat, frate = ([] for i in range(4))
    for i in streams:
        res= re.search(r'(\d+)p', str(i))
        typ= re.search(r'video/(\w+)', str(i))
        fps= re.search(r'(\d+)fps', str(i))
        tag= re.search(r'(\d+)',str(i))
        itag.append(str(i)[tag.start():tag.end()])
        resolutions.append(str(i)[res.start():res.end()])
        vformat.append(str(i)[typ.start():typ.end()])
        frate.append(str(i)[fps.start():fps.end()])
    details["resolutions"]= resolutions
    details["itag"]= itag
    details["fps"]= frate
    details["format"]= vformat
    return details


st.title("YTAna - Site de Download do YouTube Para Ana")
st.markdown(f'<h1 style="color:#000000;font-size:24px;">{"Coloque o link do vídeo aqui 👇 em seguida aperte enter:"}</h1>', unsafe_allow_html=True)
url = st.text_input('', placeholder='https://www.youtube.com/')

if url:
    
       try:
            tmpdirname = make_tempdir()
            v_info= get_info(url)
            col1, col2= st.columns([1,1.5], gap="small")
            with st.container():
                with col1:            
                    st.image(v_info["image"])   
                with col2:
                    st.subheader("Detalhes do vídeo:")
                    # res_inp = st.selectbox('__Selecione a resolução__', v_info["resolutions"])
                    res_inp = v_info["resolutions"][0]
                    id = v_info["resolutions"].index(res_inp)    
                    # v_info["resolutions"]       
                    st.write(f"__Titulo do vídeo:__ {v_info['title']}")
                    st.write(f"__Tempo do vídeo:__ {v_info['length']} segundos")
                    # st.write(f"__Resolução:__ {v_info['resolutions'][id]}")
                    st.write(f"__Frames por segundos:__ {v_info['fps'][id]}")
                    st.write(f"__Formato do vídeo:__ {v_info['format'][id]}")
                    file_name = st.text_input('__Salvar vídeo com o nome de 🎯__', placeholder = v_info['title'])
                    st.markdown(f'<h1 style="color:#000000;font-size:16px;"><center>{"O botão para download pode demorar um pouco aparecer...."}</center></h1>', unsafe_allow_html=True)
                    if file_name:        
                        if file_name != v_info['title']:
                            file_name+=".mp4"
                    else:
                        file_name = v_info['title'] + ".mp4" 
                ds = v_info["streams"].get_highest_resolution()
                ds.download(filename= file_name,output_path=tmpdirname)
                with open(tmpdirname/file_name, "rb") as f:
                    buffer = f.read()
                st.subheader("Quando os balões aparecem o video está salvo em Downloads!🎈🎈")
                button = st.download_button(
                    label="Aperte aqui para fazer o download 🎈",
                    data=buffer,
                    file_name=file_name,
                    mime="audio/mpeg")
                

                if button:
                    with st.spinner('Downloading...'):
                        try:
                            # ds = v_info["streams"].get_highest_resolution()
                            # ds.download(filename= file_name,output_path=downloads_path)
                            st.success('Download com sucesso!!!', icon="✅")       
                            st.balloons()
                        except:
                            st.error('Error: Save with a different name!', icon="🚨")  
       except:
          st.error('Erro no  link do vídeo do YouTube, verifique por favor!', icon="🚨")
              


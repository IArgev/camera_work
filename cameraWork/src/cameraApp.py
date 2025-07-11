import ttkbootstrap as ttk
from pygrabber.dshow_graph import FilterGraph
from ttkbootstrap.constants import *
from PIL import Image,ImageTk
from pathlib import Path
from appdirs import user_data_dir
from tkinter import filedialog, messagebox, PhotoImage
import time
import cv2
import os, sys



class MainApp(ttk.Window):
    def __init__(self, title="Camera", themename="litera", iconphoto='', size=(640, 640), position=None, minsize=None, maxsize=None, resizable=(False, False), hdpi=True, scaling=None, transient=None, overrideredirect=False, alpha=1, **kwargs):
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha, **kwargs)
        self.place_window_center()
        


        # =============== RUTAS PARA CÖDIGO ===================

        
        self.BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_PATH = os.path.join(self.BASE_PATH, 'data')
        
        self.CAP_PATH = os.path.join(self.BASE_PATH, 'captures')
        


        # ================IMAGENES==================================
        
        image_path = os.path.join(DATA_PATH, "close.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.closePNG = ImageTk.PhotoImage(imagePil)

        image_path = os.path.join(DATA_PATH, "camera.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.cameraPNG = ImageTk.PhotoImage(imagePil)


        image_path = os.path.join(DATA_PATH, "history.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.historyPNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "dark_mode.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.dark_modePNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "light_mode.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.light_modePNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "dark_info.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.dark_infoPNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "light_info.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.light_infoPNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "photos.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.photosPNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "save.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.savePNG = ImageTk.PhotoImage(imagePil)
        
        image_path = os.path.join(DATA_PATH, "delete.png")
        image_path = os.path.normpath(image_path)
        imagePil = Image.open(image_path)
        self.deletePNG = ImageTk.PhotoImage(imagePil)
        
        # ==========================================================

        self.cap = None
        self.rmvWnd = False
        self.labelCap = None
        self.frame_To_Cap = None
        


        self.sup_ffbar()
        self.camera_ff()
        self.sub_ffbar()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.mainloop()

    #------------------------------------------------------------------------------------------------------------------------   

    def sup_ffbar(self):
        sup_frame = ttk.Frame(self, padding=(5,5), height=40)
        sup_frame.pack_propagate(False)
        sup_frame.pack(fill=BOTH)
        
        self.supButton_Info = ttk.Label(sup_frame, padding=(3,3), image=self.light_infoPNG, bootstyle=INFO, cursor="hand2")
        self.supButton_Info.image = self.light_infoPNG
        self.supButton_Info.pack(side=LEFT, pady=1, padx=5)
        
        self.supButton_Info.bind("<Button-1>", self.see_info) 
        self.supButton_Info.bind_all("<Key-i>", self.see_info)
        
        self.supLabel_Theme = ttk.Label(sup_frame, padding=(3,3), image=self.light_modePNG, bootstyle=DARK, cursor="hand2")
        self.supLabel_Theme.image = self.light_modePNG
        self.supLabel_Theme.pack(side=RIGHT, pady=1)

        self.supLabel_Theme.bind("<Button-1>", self.change_Theme)
        self.supLabel_Theme.bind_all("<Key-m>", self.change_Theme)
        
    def see_info(self, event=None):
        try:
            self.tfInfo.destroy()
        except AttributeError:
            pass
        
        text_info = "Enter: seleccionar cámara\nEnter: tomar foto\nS: guardar foto como\nEnter: guardar foto\nM: cambiar modo (Claro / Oscuro)\nI: ver info.\nP: ver fotos"
        self.tfInfo = ttk.Toplevel(title="Info", size=(300, 300), position=(20, 20), resizable=(False, False))
        self.Btn_cap.focus_set()
        ttk.Label(self.tfInfo, text="Atajos de teclado:", font=("Sans", 10, "bold")).pack(pady=4)
        ttk.Label(self.tfInfo, text=text_info).pack(fill=X, padx=10)
        
        ttk.Label(self.tfInfo, text="Diseñado por:\nVargas Erick - Trujillo Max - Verde Joel\nChuquihuanca Anyeli - Valdez Christ\nIng.Sistemas e informática - III ciclo\nDocente Cueva Valvidia Johnny", font=("Times New Roman", 7), anchor=CENTER, justify=CENTER).pack(side=BOTTOM, fill=X, pady=2)

    def change_Theme(self, event):
        if "litera" == self.style.theme_use():
            self.supLabel_Theme.config(image=self.dark_modePNG)
            self.supLabel_Theme.image = self.dark_modePNG
            self.supButton_Info.config(image=self.dark_infoPNG)
            self.supButton_Info.image = self.dark_infoPNG
            self.style.theme_use("darkly")
            try:
                self.frameCVPhoto.configure(bootstyle=DARK)
            except:
                pass
            try:
                self.frame_data.configure(bootstyle=DARK)
            except:
                pass
            return
        self.style.theme_use("litera")
        self.supLabel_Theme.config(image=self.light_modePNG)
        self.supLabel_Theme.image = self.light_modePNG
        self.supButton_Info.config(image=self.light_infoPNG)
        self.supButton_Info.image = self.light_infoPNG
        try:
            self.frameCVPhoto.configure(bootstyle=LIGHT)
        except:
            pass
        try:
            self.frame_data.configure(bootstyle=LIGHT)
        except:
            pass
    #------------------------------------------------------------------------------------------------------------------------   

    def camera_ff(self):
        camera_frame = ttk.Frame(self, padding=(10, 20), height=520)
        camera_frame.pack(fill=BOTH)
        
        self.frame_Camera = ttk.Frame(camera_frame, height=480, width=480)
        self.frame_Camera.pack_propagate(False)
        self.frame_Camera.pack(expand=True, fill=BOTH)

        self.show_ffcameras()


    def show_ffcameras(self):
        for widget in self.frame_Camera.winfo_children():
            widget.destroy()
        
        graph = FilterGraph()
        self.camaras = graph.get_input_devices()
        try:
            self.Btn_cap.configure(state=DISABLED)
            self.Btn_cap.unbind_all("<Return>")
        except AttributeError:
            pass

        ttk.Label(self.frame_Camera, width=20, text="Cámaras disponibles", font=("Sans", 10, "bold"), justify=CENTER).place(relx=0.5, y=180, anchor="center")

        self.combo_Cameras = ttk.Combobox(self.frame_Camera, values=self.camaras, width=24, bootstyle=INFO, state=READONLY)
        self.combo_Cameras.pack(expand=True)
        if len(self.camaras) == 0:
            self.combo_Cameras.set("Sin Cámara")
        else:
            self.combo_Cameras.set(self.camaras[0])

        self.button_Iniciar = ttk.Button(self.frame_Camera, text="Iniciar", bootstyle=SUCCESS, command=self.show_camera)
        self.button_Iniciar.pack(pady=10)

        self.combo_Cameras.bind_all("<Return>", self.show_camera)

    def show_camera(self, event=None):
        camera =  self.combo_Cameras.get()
        if camera not in self.camaras:
            return
        self.combo_Cameras.unbind_all("<Return>")
        self.Btn_cap.configure(state=NORMAL)
        self.Btn_cap.bind_all("<Return>", self.take_cap)
        
        for widget in self.frame_Camera.winfo_children():
            widget.destroy()

        indexCam = 0
        for ind, cam in enumerate(self.camaras):
            if camera == cam:
                indexCam = ind
                break

        self.cap = cv2.VideoCapture(indexCam)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 620)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


        self.labelCap = ttk.Label(self.frame_Camera)
        self.labelCap.pack(expand=True, fill=BOTH)

        self.actualizar_cap()

        ttk.Button(self.frame_Camera, bootstyle=DANGER, image=self.closePNG, width=6, padding=(3, -2), command=self.quit_Cam).place(x=2,y=2)

        self.labelCap.bind_all("<Escape>", self.quit_Cam)

    def quit_Cam(self, event=None):
        if self.cap:
            self.labelCap.unbind_all("<Escape>")
            self.cap.release()
        for widget in self.frm_SaveCap.winfo_children():
            widget.destroy()
        self.show_ffcameras()

    def actualizar_cap(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.rectangle(frame, (158, 88), (461, 391), (0, 255, 0), 2)
            self.frame_To_Cap = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.labelCap.imgtk = imgtk
            self.labelCap.configure(image=imgtk)

            self.frame_Camera.after(10, self.actualizar_cap)


    #------------------------------------------------------------------------------------------------------------------------   

    def sub_ffbar(self):
        sub_frame = ttk.Frame(self, padding=(5,5), height=100)
        sub_frame.pack_propagate(False)
        sub_frame.pack(fill=BOTH)

        self.Btn_photo = ttk.Button(sub_frame, padding=(24, 5), image=self.photosPNG, command=self.see_photos, bootstyle=INFO)
        self.Btn_photo.place(x=10, rely=0.5, anchor=W)
        
        self.Btn_photo.bind_all("<Key-p>", self.see_photos)

        self.Btn_cap = ttk.Button(sub_frame, padding=(10, 10), image=self.cameraPNG, bootstyle=SUCCESS, command=self.take_cap, state=DISABLED)
        self.Btn_cap.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frm_SaveCap = ttk.Frame(sub_frame, height=80, width=250, padding=(5,5))
        self.frm_SaveCap.place(relx=1, rely=0, anchor=NE)


    def see_photos(self, event=None):
        try:
            self.See_ffphotos.destroy()
        except AttributeError:
            pass
        self.See_ffphotos = ttk.Toplevel(title="Fotos guardadas", size=(520, 700), position=(20, 20), resizable=(False, False))

        self.See_ffphotos.protocol("WM_DELETE_WINDOW", self.cerrarPhoto)
        if self.labelCap is not None:
            self.labelCap.unbind_all("<Escape>")
        

        self.canvasPhoto = ttk.Canvas(self.See_ffphotos, width=520)
        scrollPhoto = ttk.Scrollbar(self.See_ffphotos, orient=VERTICAL, bootstyle=SUCCESS, command=self.canvasPhoto.yview)
        self.frameCVPhoto = ttk.Frame(self.canvasPhoto, bootstyle=(LIGHT if self.style.theme_use() == "litera" else DARK), width=500, height=600)
        self.canvasPhoto.configure(yscrollcommand=scrollPhoto.set)
        scrollPhoto.pack(side= RIGHT, expand=True, fill=BOTH)
        self.canvasPhoto.pack(side=LEFT, expand=True, fill=BOTH)

        self.frameCVPhoto.bind("<Configure>",lambda e: self.canvasPhoto.configure(scrollregion=self.canvasPhoto.bbox("all")))

        self.See_ffphotos.bind("<Enter>", lambda e:self.canvasPhoto.bind_all("<MouseWheel>", self._on_mousewheel))
        self.See_ffphotos.bind("<Leave>", lambda e:self.canvasPhoto.unbind_all("<MouseWheel>"))

        self.window = self.canvasPhoto.create_window((0, 0), window=self.frameCVPhoto, anchor="nw")

        
        def saveChange_DNI(frame: ttk.Frame, des, name, entry):
            self.time_now = time.strftime("%d-%m-%Y",time.localtime())
            if des == 1:
                DniVal = entry.get()
                try:
                    int(DniVal)
                    if len(DniVal) != 8:
                        raise ValueError
                except:
                    ttk.Label(frame, text="DNI inválido", bootstyle=DANGER, width=20, font=("Sans", 10, "bold")).place(relx=0.5, rely=0.8, anchor=S)
                    return
                
                capturas = [file for file in os.listdir(self.CAP_PATH) if file.endswith(".jpg")]
                for cap in capturas:
                    if str(DniVal) in cap:
                        ttk.Label(frame, text="DNI ya existente", bootstyle=DANGER, width=20, font=("Sans", 10, "bold")).place(relx=0.5, rely=0.8, anchor=S) 
                        return
                os.rename(os.path.join(self.CAP_PATH, name), os.path.join(self.CAP_PATH, f"{DniVal}({self.time_now}).jpg"))
                
                name = f"{DniVal}({self.time_now}).jpg"
                
            for widget in frame.winfo_children():
                widget.destroy()
                                
            ttk.Label(frame, text="DNI", font=("Sans", 12, "bold")).pack(fill=X)
            ttk.Label(frame, text=f"{name[:8]}", font=("Sans", 10)).pack(fill=X, pady=4)
            
            ttk.Button(frame, text="Cambiar DNI", bootstyle=INFO, command= lambda: change_DNI(frame, name)).pack(fill=X, padx=2, pady=8)
            ttk.Button(frame, image=self.deletePNG, bootstyle=DANGER, command= lambda frp = frame.master: delete_DNI(frp, name)).pack(fill=X, padx=2)
            
            ttk.Label(frame, text=f"{name}", font=("Sans", 8)).pack(side=BOTTOM, fill=X)
            ttk.Label(frame, text="Guardado como", font=("Sans", 10, "bold")).pack(side=BOTTOM, fill=X)
                
        
        def change_DNI(frame:ttk.Frame, nameJPG):
            if self.rmvWnd:
                return
            
            for widget in frame.winfo_children():
                widget.destroy()
            ttk.Label(frame, text="DNI", font=("Sans", 12, "bold")).pack(fill=X)
            entryNewDni = ttk.Entry(frame, bootstyle=SUCCESS)
            entryNewDni.pack(fill=X)
            entryNewDni.focus_set()
            
            ttk.Button(frame, text="Confirmar", bootstyle=WARNING, command= lambda :saveChange_DNI(frame, 1, nameJPG, entryNewDni)).pack(fill=X, padx=2, pady=8)
            ttk.Button(frame, text="Cancelar", bootstyle=DANGER, command= lambda :saveChange_DNI(frame, 0, nameJPG, entryNewDni)).pack(fill=X, padx=2)
        
        def delete_DNI(frame, nameJPG):
            if self.rmvWnd:
                return
            
            self.rmvWnd = True
            if messagebox.askquestion(title="Eliminar foto", message="Estás seguro?") == "yes":
                try:
                    for widget in frame.winfo_children():
                        widget.destroy()
                    frame.destroy()
                    os.remove(os.path.join(self.CAP_PATH, nameJPG))
                except:
                    pass
            try:
                self.See_ffphotos.focus_set()
            except:
                pass
            self.rmvWnd = False
        
        capturas = [file for file in os.listdir(self.CAP_PATH) if file.endswith(".jpg")and "temporal" not in file]
        if len(capturas) == 0:
            self.canvasPhoto.destroy()
            scrollPhoto.destroy()
            ttk.Label(self.See_ffphotos, text=f"No hay capturas\nen la ruta de destino\n{self.CAP_PATH}", anchor=(CENTER), justify=CENTER).pack(expand=True, )
        
        for cap in capturas:
            image_path = os.path.join(self.CAP_PATH, cap)
            image_path = os.path.normpath(image_path)
            photo_pill = Image.open(image_path)
            photo_pill = photo_pill.resize((300, 300))
            photo = ImageTk.PhotoImage(photo_pill)

            f = ttk.Frame(self.frameCVPhoto, height=310, width=480, padding=(5,10))
            f.pack(fill=X, padx=5, pady=5)

            limg = ttk.Label(f, image=photo, width=30)
            limg.image = photo
            limg.pack(side=LEFT)
            
            fd = ttk.Frame(f, padding=(5,15), width=180)
            fd.pack_propagate(False)
            fd.pack(side=RIGHT, expand=True, fill=BOTH)
            
            ttk.Label(fd, text="DNI", font=("Sans", 12, "bold")).pack(fill=X)
            ttk.Label(fd, text=f"{cap[:8]}", font=("Sans", 10)).pack(fill=X, pady=4)
            
            ttk.Button(fd, text="Cambiar DNI", bootstyle=INFO, command= lambda fr=fd, name=cap:change_DNI(fr, name)).pack(fill=X, padx=2, pady=8)
            ttk.Button(fd, image=self.deletePNG, bootstyle=DANGER, command= lambda fr=f, name=cap: delete_DNI(fr, name)).pack(fill=X, padx=2)
            
            ttk.Label(fd, text=f"{cap}", font=("Sans", 8)).pack(side=BOTTOM, fill=X)
            ttk.Label(fd, text="Guardado como", font=("Sans", 10, "bold")).pack(side=BOTTOM, fill=X)
            

    def _on_mousewheel(self, event):
        self.canvasPhoto.yview_scroll(-1 * (event.delta // 120), "units")


    def take_cap(self, event=None):
        self.capture = self.frame_To_Cap[90:390, 160:460]
        cv2.imwrite(os.path.join(self.CAP_PATH, "temporal.jpg"), self.capture)
        for widget in self.frm_SaveCap.winfo_children():
            widget.destroy()
            
        if os.path.isfile(f"{self.CAP_PATH}\\temporal.jpg"):
            ttk.Label(self.frm_SaveCap, text="Captura, tomada", justify="center", padding=(10,0), font=("Sans", 12, "bold")).pack(padx=5)
            self.toSave_Cap = ttk.Button(self.frm_SaveCap, text="Guardar", bootstyle=INFO, command=self.save_tfCap, padding=(15, 5))
            self.toSave_Cap.pack(padx=5, pady=2)
            self.toSave_Cap.bind_all("<Key-s>", self.save_tfCap)
        else:
            ttk.Label(self.frm_SaveCap, text="No se tomó la captura", justify="center", padding=(10,5), font=("Sans", 12, "bold")).pack(padx=5, pady=2)

    def save_tfCap(self, event=None):

        try:
            self.See_ffphotos.destroy()
        except AttributeError:
            pass
        
        self.Save_ffphoto = ttk.Toplevel(title="Guadar foto", size=(580, 480), position=(self.winfo_screenwidth()-620, 20), resizable=(False, False))
        self.Save_ffphoto.grab_set()

        self.toSave_Cap.unbind_all("<Key-s>")
        self.Btn_cap.unbind_all("<Return>")
        self.labelCap.unbind_all("<Escape>")
        self.Btn_photo.unbind_all("<Key-p>")
        self.supButton_Info.unbind_all("<Key-i>")
        

        self.Save_ffphoto.protocol("WM_DELETE_WINDOW", self.cerrarSave)
        ttk.Label(self.Save_ffphoto, text="Registro de datos", bootstyle="inversed-info", font=("Sans", 16, "bold"), anchor=CENTER, padding=(0, 10)).pack(fill=X)

        self.frame_data = ttk.Frame(self.Save_ffphoto, bootstyle=(LIGHT if self.style.theme_use() == "litera" else DARK), padding=(10, 10))
        self.frame_data.pack(expand=True, fill=BOTH, padx=5, pady=5)

        frame_path = ttk.Frame(self.frame_data)
        frame_path.pack(side=TOP, fill=X)

        def change_Path():
            nueva_ruta = filedialog.askdirectory(initialdir=self.CAP_PATH, title="Destino de capturas")
            
            if nueva_ruta:
                
                if "ñ" in nueva_ruta:
                    ttk.Label(self.frame_subData, text="Ruta inválida", bootstyle=DANGER, font=("Sans", 10, "bold")).place(relx=0.5, rely=0.8, anchor=S)
                    return                
                entry_path.configure(state=NORMAL)
                entry_path.delete(0, END)
                entry_path.insert(0, nueva_ruta)
                entry_path.configure(state=READONLY)
                os.remove(os.path.join(self.CAP_PATH, "temporal.jpg"))
                nueva_ruta = Path(nueva_ruta).expanduser().resolve()
                nueva_ruta.mkdir(parents=True, exist_ok=True)
                self.CAP_PATH = nueva_ruta
                cv2.imwrite(os.path.join(self.CAP_PATH, "temporal.jpg"), self.capture)
            else:
                nueva_ruta = os.path.join(self.BASE_PATH, 'captures')
                entry_path.configure(state=NORMAL)
                entry_path.delete(0, END)
                entry_path.insert(0, nueva_ruta)
                entry_path.configure(state=READONLY)
                os.remove(os.path.join(self.CAP_PATH, "temporal.jpg"))
                self.CAP_PATH = nueva_ruta
                cv2.imwrite(os.path.join(self.CAP_PATH, "temporal.jpg"), self.capture)
                    
                    
        def formatDNI(event):
            texto = self.entry_DNI.get()
            if len(texto) <= 8:
                textFormat.config(text=f"{texto}({self.time_now}).jpg")
            if event.keysym == "Return":
                self.save_Cap()

        ttk.Label(frame_path, text="Ruta de destino").pack(side=TOP, fill=X)

        entry_path = ttk.Entry(frame_path, width=70)
        entry_path.pack(side=LEFT, padx=5, pady=5)
        entry_path.insert(0, self.CAP_PATH)
        entry_path.configure(state=READONLY)

        ttk.Button(frame_path, text="Cambiar ruta", bootstyle=SUCCESS, padding=(5,2), command=change_Path).pack(side=RIGHT, padx=5)

        image_path = os.path.join(self.CAP_PATH, "temporal.jpg")
        image_path = os.path.normpath(image_path)
        photo_pill = Image.open(image_path)
        photo_pill = photo_pill.resize((300, 300))
        photo = ImageTk.PhotoImage(photo_pill)

        lblpht = ttk.Label(self.frame_data, image=photo, width=30)
        lblpht.pack(side=LEFT)
        lblpht.image = photo

        self.frame_subData = ttk.Frame(self.frame_data, padding=(10,5))
        self.frame_subData.pack(side=RIGHT, expand=True, fill=BOTH)

        ttk.Label(self.frame_subData, text="Datos personales", font=("Sans", 10, "bold")).pack(pady=2)
        ttk.Label(self.frame_subData, text="DNI", font=("Sans", 8, "bold")).pack(fill=X)
        self.entry_DNI = ttk.Entry(self.frame_subData, width=40)
        self.entry_DNI.pack()
        self.entry_DNI.focus_set()

        self.entry_DNI.bind("<KeyRelease>", formatDNI)

        frminfoS = ttk.Frame(self.frame_subData)
        frminfoS.pack(side=BOTTOM, fill=X)
        frminfo = ttk.Frame(frminfoS)
        frminfo.pack(side=LEFT, expand=True, fill=BOTH)
        ttk.Label(frminfo, text="Guardar como").pack(fill=X)

        self.time_now = time.strftime("%d-%m-%Y",time.localtime())

        textFormat = ttk.Label(frminfo, text=f"-{self.time_now}.jpg")
        textFormat.pack(expand=True, fill=X)

        self.Button_SaveCap = ttk.Button(frminfoS, text="Guardar", padding=(3,5), command=self.save_Cap)
        self.Button_SaveCap.pack(side=RIGHT)

    def save_Cap(self, event=None):
        DniVal = self.entry_DNI.get()
        try:
            int(DniVal)
            if len(DniVal) != 8:
                raise ValueError
        except:
            ttk.Label(self.frame_subData, text="DNI inválido", bootstyle=DANGER, font=("Sans", 10, "bold"), width=25, anchor=CENTER).place(relx=0.5, rely=0.8, anchor=S)
            return
        capturas = [file for file in os.listdir(self.CAP_PATH) if file.endswith(".jpg")]
        for cap in capturas:
            if str(DniVal) in cap:
                ttk.Label(self.frame_subData, text="DNI existente", bootstyle=DANGER, font=("Sans", 10, "bold"), width=25, anchor=CENTER).place(relx=0.5, rely=0.8, anchor=S)
                return
        os.rename(os.path.join(self.CAP_PATH, "temporal.jpg"),os.path.join(self.CAP_PATH, f"{DniVal}({self.time_now}).jpg"))
        self.cerrarSave()
        


    #------------------------------------------------------------------------------------------------------------------------   

    def cerrar(self):
        if self.cap:
            self.cap.release()
        if self.frame_To_Cap is not None and os.path.isfile(f"{self.CAP_PATH}\\temporal.jpg"):
            os.remove(f"{self.CAP_PATH}\\temporal.jpg")
        self.destroy()

    def cerrarSave(self):
        self.Save_ffphoto.destroy()
        self.toSave_Cap.unbind_all("<Key-s>")
        self.Btn_cap.bind_all("<Return>", self.take_cap)
        self.labelCap.bind_all("<Escape>", self.quit_Cam)
        self.Btn_photo.bind_all("<Key-p>", self.see_photos)
        self.supButton_Info.bind_all("<Key-i>", self.see_info)
        
        
        
        for widget in self.frm_SaveCap.winfo_children():
            widget.destroy()
            
    def cerrarPhoto(self):
        if self.labelCap is not None:
            self.labelCap.bind_all("<Escape>", self.quit_Cam)
        for widget in self.See_ffphotos.winfo_children():
            widget.destroy()
        self.Btn_cap.focus_set()
        self.See_ffphotos.destroy()

    def place_window_center(self):
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height.
        RECUPERADO DE TTKBOOTSTRAP DOCUMENTATION."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

root = MainApp()
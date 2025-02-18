import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Rutas predeterminadas para cada tamaño de imagen
default_paths = {
    2048: r"\\10.20.20.20\Projects\coinhunt-user\Coin_Hunt\Arte\3D_Cubies\Cubie Skins\1_RENDER\Cubies_Renders_2k",
    512: r"\\10.20.20.20\Projects\coinhunt-user\Coin_Hunt\Arte\3D_Cubies\Cubie Skins\1_RENDER\Cubies_Renders_512",
    420: r"\\10.20.20.20\Projects\coinhunt-user\Coin_Hunt\Arte\3D_Cubies\Cubie Skins\1_RENDER\Cubies_Renders_420",
}

def select_image():
    global img, img_display, image_name, image_extension
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_path:
        img = Image.open(file_path)
        img_display = ImageTk.PhotoImage(img.resize((200, 200), Image.LANCZOS))
        image_label.config(image=img_display)
        current_dimensions_label.config(text=f"Dimensiones actuales: {img.width} x {img.height}")
        
        # Obtener el nombre del archivo y su extensión
        image_name, image_extension = os.path.splitext(os.path.basename(file_path))
        
        # Actualizar las rutas con las predeterminadas
        export_entry_512.delete(0, tk.END)
        export_entry_512.insert(0, default_paths[512])
        
        export_entry_420.delete(0, tk.END)
        export_entry_420.insert(0, default_paths[420])
        
        export_entry_2048.delete(0, tk.END)
        export_entry_2048.insert(0, default_paths[2048])
        
        export_button.config(state=tk.NORMAL)

def select_all_text(event):
    """Seleccionar todo el texto actual al hacer clic en un campo."""
    event.widget.select_range(0, tk.END)
    event.widget.icursor(tk.END)

def export_images():
    global img, image_name, image_extension
    dimensions = [(512, 512), (420, 420), (2048, 2048)]
    paths = [export_entry_512.get(), export_entry_420.get(), export_entry_2048.get()]
    
    for dim, base_path in zip(dimensions, paths):
        # Verificar que la ruta base es válida
        if not os.path.exists(base_path):
            messagebox.showerror("Error", f"La ruta '{base_path}' no existe.")
            return
        
        # Construir la ruta completa con el nombre y la extensión
        full_path = os.path.join(base_path, f"{image_name}_{dim[0]}x{dim[1]}{image_extension}")
        
        try:
            img_resized = img.resize(dim, Image.LANCZOS)
            img_resized.save(full_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la imagen {dim[0]}x{dim[1]}: {e}")
            return

    messagebox.showinfo("Éxito", "Las imágenes se exportaron exitosamente.")

# Crear la ventana principal
root = tk.Tk()
root.title("Reescalador de Texturas")
root.geometry("600x700")

# Etiqueta para mostrar la imagen
image_label = tk.Label(root, text="Selecciona una imagen", borderwidth=2, relief="solid")
image_label.pack(pady=10)

# Botón para seleccionar imagen
select_button = tk.Button(root, text="Seleccionar Imagen", command=select_image)
select_button.pack(pady=10)

# Etiqueta para mostrar las dimensiones actuales
current_dimensions_label = tk.Label(root, text="Dimensiones actuales: -")
current_dimensions_label.pack()

# Campo para 512x512
export_label_512 = tk.Label(root, text="Ruta base para exportación (512x512):")
export_label_512.pack()
export_entry_512 = tk.Entry(root, width=50)
export_entry_512.pack(pady=5)
export_entry_512.bind("<FocusIn>", select_all_text)  # Seleccionar texto al hacer clic

# Campo para 420x420
export_label_420 = tk.Label(root, text="Ruta base para exportación (420x420):")
export_label_420.pack()
export_entry_420 = tk.Entry(root, width=50)
export_entry_420.pack(pady=5)
export_entry_420.bind("<FocusIn>", select_all_text)  # Seleccionar texto al hacer clic

# Campo para 2048x2048
export_label_2048 = tk.Label(root, text="Ruta base para exportación (2048x2048):")
export_label_2048.pack()
export_entry_2048 = tk.Entry(root, width=50)
export_entry_2048.pack(pady=5)
export_entry_2048.bind("<FocusIn>", select_all_text)  # Seleccionar texto al hacer clic

# Botón para exportar
export_button = tk.Button(root, text="Exportar", command=export_images, state=tk.DISABLED)
export_button.pack(pady=20)

root.mainloop()

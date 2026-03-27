"""
Baúl de los Recuerdos - Aplicación de gestión de recuerdos personales.

Este sistema permite registrar, editar, eliminar, buscar y visualizar recuerdos
mediante una interfaz gráfica desarrollada con Tkinter.

Arquitectura:
- Data Layer: Modelo de datos (Recuerdo)
- Repository Layer: Manejo de almacenamiento
- Logic Layer: Validaciones y reglas de negocio
- GUI Layer: Interfaz gráfica

@author Robert Cerón
@version 1.0.0
"""

from __future__ import annotations
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, simpledialog
from datetime import datetime


# ***************
# DATA LAYER
# ***************
@dataclass
class Recuerdo:
    """
    Representa un recuerdo dentro del sistema.

    Atributos:
        nombre_recuerdo (str): Nombre del recuerdo.
        categoria (str): Categoría principal.
        subcategoria (str): Subcategoría del recuerdo.
        descripcion (str): Descripción detallada.
        fecha (str): Fecha asociada (DD/MM/YYYY).
        estado (str): Estado del recuerdo (Nuevo, Usado, Deteriorado).
    """
    nombre_recuerdo: str
    categoria: str
    subcategoria: str
    descripcion: str
    fecha: str
    estado: str


class BaulRecuerdosRepositorio:
    """
    Gestiona el almacenamiento de recuerdos en memoria.

    Funciona como una base de datos simple basada en lista.
    """

    def __init__(self):
        """Inicializa la lista de recuerdos vacía."""
        self.recuerdos = []

    def agregar_recuerdo(self, recuerdo):
        """
        Agrega un recuerdo al repositorio.

        Args:
            recuerdo (Recuerdo): Objeto a almacenar.
        """
        self.recuerdos.append(recuerdo)

    def obtener_recuerdos(self):
        """
        Retorna todos los recuerdos almacenados.

        Returns:
            list: Lista de recuerdos.
        """
        return self.recuerdos

    def eliminar_recuerdo(self, index):
        """
        Elimina un recuerdo según su índice.

        Args:
            index (int): Posición en la lista.
        """
        del self.recuerdos[index]

    def actualizar_recuerdo(self, index, recuerdo):
        """
        Actualiza un recuerdo existente.

        Args:
            index (int): Posición del recuerdo.
            recuerdo (Recuerdo): Nuevo objeto actualizado.
        """
        self.recuerdos[index] = recuerdo


# ***************
# LOGIC LAYER
# ***************
class BaulRecuerdosServicio:
    """
    Contiene la lógica de negocio del sistema.

    Se encarga de validar datos antes de enviarlos al repositorio.
    """

    def __init__(self, repositorio):
        """
        Inicializa el servicio con un repositorio.

        Args:
            repositorio (BaulRecuerdosRepositorio): Fuente de datos.
        """
        self.repositorio = repositorio

    def registrar_recuerdo(self, nombre, categoria, subcategoria, descripcion, fecha, estado):
        """
        Registra un nuevo recuerdo validando los datos.

        Raises:
            ValueError: Si faltan campos obligatorios.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del recuerdo es obligatorio")

        if not categoria or not categoria.strip():
            raise ValueError("La categoría es obligatoria")

        if not estado or estado == "Seleccione":
            raise ValueError("El estado es obligatorio")

        if not fecha or not fecha.strip():
            fecha = datetime.now().strftime("%d/%m/%Y")

        recuerdo = Recuerdo(
            nombre.strip(),
            categoria.strip(),
            subcategoria.strip(),
            descripcion.strip(),
            fecha.strip(),
            estado.strip()
        )

        self.repositorio.agregar_recuerdo(recuerdo)

    def listar_recuerdos(self):
        """
        Obtiene todos los recuerdos.

        Returns:
            list: Lista de recuerdos.
        """
        return self.repositorio.obtener_recuerdos()

    def eliminar_recuerdo(self, index):
        """
        Elimina un recuerdo.

        Args:
            index (int): Índice del recuerdo.
        """
        self.repositorio.eliminar_recuerdo(index)

    def editar_recuerdo(self, index, nombre, categoria, subcategoria, descripcion, fecha, estado):
        """
        Edita un recuerdo existente.

        Raises:
            ValueError: Si los datos no son válidos.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")

        if not estado or estado == "Seleccione":
            raise ValueError("El estado es obligatorio")

        if not fecha or not fecha.strip():
            fecha = datetime.now().strftime("%d/%m/%Y")

        recuerdo = Recuerdo(
            nombre.strip(),
            categoria.strip(),
            subcategoria.strip(),
            descripcion.strip(),
            fecha.strip(),
            estado.strip()
        )

        self.repositorio.actualizar_recuerdo(index, recuerdo)


# ***************
# GUI
# ***************
class AppBaulRecuerdos:
    """
    Interfaz gráfica principal del sistema.

    Permite al usuario interactuar con el sistema de recuerdos.
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal.

        Args:
            root (tk.Tk): Ventana principal.
        """
        self.root = root
        self.root.title("Baúl de los Recuerdos")
        self.root.geometry("850x850")
        self.root.configure(bg="#f2e6d9")

        self.repositorio = BaulRecuerdosRepositorio()
        self.servicio = BaulRecuerdosServicio(self.repositorio)
        self.categorias = ["Juguetes", "Videojuegos", "Deportes", "Música", "Coleccionables", "Otro"]

        self._construir_ui()

    def _construir_ui(self):
        """
        Construye todos los componentes visuales de la aplicación.
        """
        main = tk.Frame(self.root, bg="#f2e6d9", padx=20, pady=20)
        main.pack(fill="both", expand=True)

        titulo = tk.Label(
            main, text="🧰 Baúl de los Recuerdos",
            font=("Georgia", 20, "bold"), bg="#f2e6d9", fg="#5a3e2b"
        )
        titulo.pack(pady=10)

        frame_registro = tk.LabelFrame(
            main, text="Guardar / Editar recuerdo",
            padx=15, pady=15, bg="#fffaf5", fg="#5a3e2b", font=("Georgia", 11, "bold")
        )
        frame_registro.pack(fill="x", pady=10)

        tk.Label(frame_registro, text="Nombre:", bg="#fffaf5").grid(row=0, column=0, sticky="w")
        self.nombre_entry = tk.Entry(frame_registro, width=35)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame_registro, text="Categoría:", bg="#fffaf5").grid(row=1, column=0, sticky="w")
        self.categoria_var = tk.StringVar(value="Seleccione")
        self.categoria_menu = tk.OptionMenu(frame_registro, self.categoria_var, *self.categorias, command=self.verificar_categoria)
        self.categoria_menu.config(width=32)
        self.categoria_menu.grid(row=1, column=1, pady=5)

        tk.Label(frame_registro, text="Subcategoría:", bg="#fffaf5").grid(row=2, column=0, sticky="w")
        self.subcategoria_entry = tk.Entry(frame_registro, width=35)
        self.subcategoria_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame_registro, text="Fecha :", bg="#fffaf5").grid(row=3, column=0, sticky="w")
        self.fecha_entry = tk.Entry(frame_registro, width=35)
        self.fecha_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame_registro, text="Estado:", bg="#fffaf5").grid(row=4, column=0, sticky="w")
        self.estado_var = tk.StringVar(value="Seleccione")
        self.estado_menu = tk.OptionMenu(frame_registro, self.estado_var, "Nuevo", "Usado", "Deteriorado")
        self.estado_menu.config(width=32)
        self.estado_menu.grid(row=4, column=1, pady=5)

        tk.Label(frame_registro, text="Descripción:", bg="#fffaf5").grid(row=5, column=0, sticky="w")
        self.descripcion_entry = tk.Entry(frame_registro, width=35)
        self.descripcion_entry.grid(row=5, column=1, pady=5)

        tk.Button(frame_registro, text="Guardar Recuerdo", command=self.agregar_recuerdo,
                  bg="#5a3e2b", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

        botones = tk.Frame(main, bg="#f2e6d9")
        botones.pack(pady=5)

        tk.Button(botones, text="✏️ Editar", command=self.editar_recuerdo,
                  bg="#5a3e2b", fg="white").grid(row=0, column=0, padx=5)

        tk.Button(botones, text="🗑 Eliminar", command=self.eliminar_recuerdo,
                  bg="#5a3e2b", fg="white").grid(row=0, column=1, padx=5)

        tk.Button(botones, text="📑 Reporte", command=self.reporte_recuerdos,
                  bg="#5a3e2b", fg="white").grid(row=0, column=2, padx=5)

        tk.Label(main, text="🔍 Buscar (nombre, categoría, fecha, estado):", bg="#f2e6d9").pack()
        self.busqueda_entry = tk.Entry(main, width=40)
        self.busqueda_entry.pack(pady=5)

        tk.Button(main, text="Buscar", command=self.buscar_recuerdos,
                  bg="#5a3e2b", fg="white").pack(pady=5)

        frame_lista = tk.LabelFrame(
            main, text="Mis Recuerdos Guardados",
            padx=15, pady=15, bg="#fffaf5", fg="#5a3e2b", font=("Georgia", 11, "bold")
        )
        frame_lista.pack(fill="both", expand=True, pady=10)

        self.lista_recuerdos = tk.Listbox(
            frame_lista, width=100, height=20, bg="#fdf6ec", fg="#4a2f1c", font=("Arial", 11)
        )
        self.lista_recuerdos.pack()

        self.lista_recuerdos.bind("<<ListboxSelect>>", self.seleccionar_recuerdo)

        self.descripcion_label = tk.Label(
            main,
            text="Selecciona un recuerdo para ver su descripción",
            wraplength=800,
            justify="left",
            bg="#f2e6d9",
            fg="#4a2f1c",
            font=("Arial", 10, "italic")
        )
        self.descripcion_label.pack(pady=10)

        tk.Button(main, text="Actualizar Lista", command=self.mostrar_recuerdos,
                  bg="#5a3e2b", fg="white").pack(pady=10)

    # FUNCIONES UI DOCUMENTADAS
    def verificar_categoria(self, seleccion):
        """Permite agregar una nueva categoría si el usuario selecciona 'Otro'."""
        if seleccion == "Otro":
            nueva = simpledialog.askstring("Nueva categoría", "Escribe una nueva categoría:")
            if nueva and nueva.strip():
                self.categorias.insert(-1, nueva.strip())
                self.actualizar_menu()
                self.categoria_var.set(nueva.strip())
            else:
                self.categoria_var.set("Seleccione")

    def actualizar_menu(self):
        """Actualiza dinámicamente el menú de categorías."""
        menu = self.categoria_menu["menu"]
        menu.delete(0, "end")
        for cat in self.categorias:
            menu.add_command(label=cat, command=lambda value=cat: self.categoria_var.set(value))

    def agregar_recuerdo(self):
        """Captura datos del formulario y registra un recuerdo."""
        try:
            if self.categoria_var.get() == "Seleccione":
                raise ValueError("Debe seleccionar una categoría")

            self.servicio.registrar_recuerdo(
                self.nombre_entry.get(),
                self.categoria_var.get(),
                self.subcategoria_entry.get(),
                self.descripcion_entry.get(),
                self.fecha_entry.get() if self.fecha_entry.get().strip() else datetime.now().strftime("%d/%m/%Y"),
                self.estado_var.get()
            )

            self.limpiar_campos()
            self.mostrar_recuerdos()
            messagebox.showinfo("Guardado", "Recuerdo guardado correctamente")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_recuerdos(self):
        """Muestra todos los recuerdos en la lista."""
        self.lista_recuerdos.delete(0, tk.END)
        self.recuerdos_actuales = self.servicio.listar_recuerdos()

        for r in self.recuerdos_actuales:
            self.lista_recuerdos.insert(
                tk.END,
                f"📝 {r.nombre_recuerdo} | 📂 {r.categoria} | 🏷 {r.subcategoria} | 📅 {r.fecha} | ⚡ {r.estado} | 📖 {r.descripcion}"
            )

    def seleccionar_recuerdo(self, event):
        """Carga en el formulario el recuerdo seleccionado."""
        if self.lista_recuerdos.curselection():
            i = self.lista_recuerdos.curselection()[0]
            r = self.recuerdos_actuales[i]

            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, r.nombre_recuerdo)

            self.categoria_var.set(r.categoria)

            self.subcategoria_entry.delete(0, tk.END)
            self.subcategoria_entry.insert(0, r.subcategoria)

            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, r.fecha)

            self.estado_var.set(r.estado)

            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, r.descripcion)

            self.descripcion_label.config(text=f"📖 {r.descripcion}")

    def eliminar_recuerdo(self):
        """Elimina un recuerdo con confirmación."""
        if self.lista_recuerdos.curselection():
            i = self.lista_recuerdos.curselection()[0]
            r = self.recuerdos_actuales[i]

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar el recuerdo '{r.nombre_recuerdo}'?"
            )

            if confirmar:
                self.servicio.eliminar_recuerdo(i)
                self.mostrar_recuerdos()
                messagebox.showinfo("Eliminado", "Recuerdo eliminado correctamente")

    def editar_recuerdo(self):
        """Abre ventana emergente para editar un recuerdo."""
        if self.lista_recuerdos.curselection():
            i = self.lista_recuerdos.curselection()[0]
            r = self.recuerdos_actuales[i]

            popup = tk.Toplevel(self.root)
            popup.title(f"Editar Recuerdo: {r.nombre_recuerdo}")
            popup.geometry("400x450")
            popup.configure(bg="#f2e6d9")

            tk.Label(popup, text="Editar Recuerdo", font=("Georgia", 14, "bold"),
                     bg="#f2e6d9", fg="#5a3e2b").pack(pady=10)

            tk.Label(popup, text="Nombre:", bg="#f2e6d9").pack(anchor="w", padx=10)
            nombre_edit = tk.Entry(popup, width=40)
            nombre_edit.pack(pady=5)
            nombre_edit.insert(0, r.nombre_recuerdo)

            tk.Label(popup, text="Categoría:", bg="#f2e6d9").pack(anchor="w", padx=10)
            categoria_var_edit = tk.StringVar(value=r.categoria)
            tk.OptionMenu(popup, categoria_var_edit, *self.categorias).pack(pady=5)

            tk.Label(popup, text="Subcategoría:", bg="#f2e6d9").pack(anchor="w", padx=10)
            subcategoria_edit = tk.Entry(popup, width=40)
            subcategoria_edit.pack(pady=5)
            subcategoria_edit.insert(0, r.subcategoria)

            tk.Label(popup, text="Fecha:", bg="#f2e6d9").pack(anchor="w", padx=10)
            fecha_edit = tk.Entry(popup, width=40)
            fecha_edit.pack(pady=5)
            fecha_edit.insert(0, r.fecha)

            tk.Label(popup, text="Estado:", bg="#f2e6d9").pack(anchor="w", padx=10)
            estado_var_edit = tk.StringVar(value=r.estado)
            tk.OptionMenu(popup, estado_var_edit, "Nuevo", "Usado", "Deteriorado").pack(pady=5)

            tk.Label(popup, text="Descripción:", bg="#f2e6d9").pack(anchor="w", padx=10)
            descripcion_edit = tk.Entry(popup, width=40)
            descripcion_edit.pack(pady=5)
            descripcion_edit.insert(0, r.descripcion)

            def guardar_cambios():
                """Guarda los cambios realizados en el recuerdo."""
                try:
                    if categoria_var_edit.get() == "Seleccione":
                        raise ValueError("Debe seleccionar una categoría")

                    self.servicio.editar_recuerdo(
                        i,
                        nombre_edit.get(),
                        categoria_var_edit.get(),
                        subcategoria_edit.get(),
                        descripcion_edit.get(),
                        fecha_edit.get(),
                        estado_var_edit.get()
                    )

                    self.mostrar_recuerdos()
                    self.descripcion_label.config(text=f"📖 {descripcion_edit.get()}")
                    popup.destroy()

                    messagebox.showinfo("Editado", "Recuerdo actualizado correctamente")

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(popup, text="Guardar Cambios", command=guardar_cambios,
                      bg="#5a3e2b", fg="white").pack(pady=15)

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self.nombre_entry.delete(0, tk.END)
        self.subcategoria_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.categoria_var.set("Seleccione")
        self.estado_var.set("Seleccione")

    def buscar_recuerdos(self):
        """Filtra recuerdos según criterio de búsqueda."""
        criterio = self.busqueda_entry.get().lower()
        self.lista_recuerdos.delete(0, tk.END)

        for r in self.servicio.listar_recuerdos():
            if (criterio in r.nombre_recuerdo.lower() or
                criterio in r.categoria.lower() or
                criterio in r.fecha.lower() or
                criterio in r.estado.lower()):

                self.lista_recuerdos.insert(
                    tk.END,
                    f"📝 {r.nombre_recuerdo} | 📂 {r.categoria} | 🏷 {r.subcategoria} | 📅 {r.fecha} | ⚡ {r.estado} | 📖 {r.descripcion}"
                )

    def reporte_recuerdos(self):
        """Genera un reporte de todos los recuerdos."""
        recuerdos = self.servicio.listar_recuerdos()

        if not recuerdos:
            messagebox.showinfo("Reporte", "No hay recuerdos guardados.")
            return

        reporte = "\n".join(
            [f"📝 {r.nombre_recuerdo} | 📂 {r.categoria} | 🏷 {r.subcategoria} | 📅 {r.fecha} | ⚡ {r.estado} | 📖 {r.descripcion}" for r in recuerdos]
        )

        messagebox.showinfo("Reporte de Recuerdos", reporte)


def main():
    """Punto de entrada principal de la aplicación."""
    root = tk.Tk()
    app = AppBaulRecuerdos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
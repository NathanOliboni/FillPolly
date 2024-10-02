import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, colorchooser
from shapely.geometry import Polygon, Point

class PolygonDrawer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Desenhador de Polígonos")
        self.geometry("1080x720")
        
        # Layout principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame do canvas para desenhar
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Canvas onde os polígonos são desenhados
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="white", width=600, height=400)
        self.canvas.pack(pady=20)
        
        # Frame para a lista de polígonos
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.grid(row=0, column=1, padx=20, pady=20)
        
        # Título da lista de polígonos
        self.list_label = ctk.CTkLabel(self.list_frame, text="Lista de Polígonos")
        self.list_label.pack(pady=10)
        
        # Área onde os botões de polígonos serão listados
        self.polygon_list_box = ctk.CTkFrame(self.list_frame)
        self.polygon_list_box.pack(fill="both", expand=True)
        
        # Botões
        self.clear_button = ctk.CTkButton(self.main_frame, text="Limpar Tela", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.delete_button = ctk.CTkButton(self.main_frame, text="Excluir Polígono", command=self.delete_polygon)
        self.delete_button.grid(row=1, column=1, padx=10, pady=10)
        
        self.paint_button = ctk.CTkButton(self.main_frame, text="Preencher Polígono", command=self.fillpoly)
        self.paint_button.grid(row=2, column=1, padx=10, pady=10)
        
        # Botão para selecionar a cor
        self.color_button = ctk.CTkButton(self.main_frame, text="Selecionar Cor", command=self.choose_color)
        self.color_button.grid(row=2, column=0, padx=10, pady=10)
        
        # Botão para selecionar a cor da aresta
        self.color_button = ctk.CTkButton(self.main_frame, text="Selecionar Cor da Aresta", command=self.choose_edge_color)
        self.color_button.grid(row=3, column=0, padx=10, pady=10)

        # Variáveis para armazenamento
        self.polygons = []  # Lista de polígonos (armazena coordenadas)
        self.current_polygon = []  # Ponto temporário
        self.selected_polygon = None  # Índice do polígono selecionado
        self.current_color = "black"  # Cor padrão para o desenho
        self.color2paint = ""
        self.color2edge = "yellow"
        self.colorsList = [] # Lista para armazenar as cores para redesenhar caso algum seja excluido
        
        # Adiciona um círculo para exibir a cor selecionada
        self.color_display = self.canvas.create_oval(620, 20, 650, 50, fill=self.current_color, outline="yellow", width=2)
        
        # Eventos do mouse
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Double-Button-1>", self.finish_polygon)  # Fechar polígono com duplo clique
        self.canvas.bind("<Button-3>", self.select_polygon)
        
    def choose_color(self):
        """ Abre um seletor de cor e atualiza a cor atual e a exibição da cor."""
        color_code = colorchooser.askcolor(title="Escolher Cor")[1]  # Retorna uma tupla (RGB, Hex), pegamos o Hex
        if color_code:
            # self.current_color = color_code # Valor Hex
            self.color2paint = color_code # Valor Hex
            self.canvas.itemconfig(self.color_display, fill=self.current_color)
            
    def choose_edge_color(self):
        """ Abre um seletor de cor e atualiza a cor atual e a exibição da cor."""
        color_code = colorchooser.askcolor(title="Escolher Cor")[1]
        if color_code:
            self.color2edge = color_code
            self.canvas.itemconfig(self.color_display, fill=self.current_color)
            
    def add_point(self, event):
        """ Adiciona um ponto ao polígono atual."""
        x, y = event.x, event.y
        self.current_polygon.append((x, y))
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
        
        # Desenha linhas entre pontos
        if len(self.current_polygon) > 1:
            # A linha deve ser mais grossa para melhor visualização
            self.add_point_line = self.canvas.create_line(self.current_polygon[-2], self.current_polygon[-1], fill=self.color2edge, width=4)
    
    def finish_polygon(self, event=None):
        """ Conclui o desenho de um polígono e o armazena."""
        if len(self.current_polygon) > 2:
            # Fechar o polígono desenhando uma linha do último ponto para o primeiro
            self.add_point_line = self.canvas.create_line(self.current_polygon[-1], self.current_polygon[0], fill=self.color2edge, width=4)
            
            # Adiciona o polígono à lista
            self.polygons.append(self.current_polygon)
            self.colorsList.append('')
            self.current_polygon = []  # Reseta para o próximo desenho
            
            # Atualiza a lista de polígonos no frame lateral
            self.list_polygons()
        else:
            messagebox.showerror("Erro", "Um polígono precisa ter pelo menos 3 pontos.")
        # Printar as coordenadas dos polígonos desenhados
        print(self.polygons)
        print(self.colorsList)
    
    def select_polygon(self, event):
        """Seleciona o polígono sobre o qual o usuário clicou."""
        x, y = event.x, event.y
        clicked_point = Point(x, y)
        for idx, polygon in enumerate(self.polygons):
            poly_shape = Polygon(polygon)  # Utiliza a biblioteca Shapely para tratar polígonos
            if poly_shape.contains(clicked_point):
                self.selected_polygon = idx
                messagebox.showinfo("Seleção", f"Polígono {idx+1} selecionado")
                return
        
        messagebox.showinfo("Seleção", "Nenhum polígono encontrado no ponto clicado.")
    
    def delete_polygon(self):
        """ Exclui o polígono selecionado da lista e do canvas."""
        if self.selected_polygon is not None and 0 <= self.selected_polygon < len(self.polygons):
            # Exclui o polígono selecionado
            del self.polygons[self.selected_polygon]
            del self.colorsList[self.selected_polygon]
            
            # Resetar a seleção
            self.selected_polygon = None
            
            # Limpa o canvas e redesenha os polígonos restantes
            # Passar a self.polygons para uma lista de polígonos auxiliar
            self.polygons_aux = self.polygons.copy()
            
            self.clear_canvas()  # Chama apenas para limpar o canvas
            self.redraw()  # Redesenha os polígonos restantes

            # Atualiza a lista de polígonos no frame lateral
            self.list_polygons()
        else:
            messagebox.showwarning("Atenção", "Nenhum polígono selecionado ou seleção inválida.")
    
    def list_polygons(self):
        """ Atualiza a lista de polígonos desenhados no frame lateral."""
        # Limpa a lista atual de botões
        for widget in self.polygon_list_box.winfo_children():
            widget.destroy()
        
        if not self.polygons:
            no_poly_label = ctk.CTkLabel(self.polygon_list_box, text="Nenhum polígono desenhado.")
            no_poly_label.pack(pady=10)
            return
        
        for idx, polygon in enumerate(self.polygons):
            polygon_button = ctk.CTkButton(self.polygon_list_box, text=f"Polígono {idx+1}", 
            command=lambda i=idx: self.select_polygon_from_list(i))
            polygon_button.pack(pady=5)

    def select_polygon_from_list(self, index):
        """ Seleciona um polígono a partir da lista exibida."""
        self.selected_polygon = index
    
    def clear_canvas(self):
        """ Limpa o canvas e reinicia a lista de pontos temporários e a lista de polígonos."""
        self.canvas.delete("all")  # Limpa o canvas
        self.current_polygon = []
        self.polygons = []  # Limpa a lista de polígonos desenhados
        self.selected_polygon = None  # Reseta a seleção

        # Atualiza a lista de polígonos no frame lateral
        self.list_polygons()
        
    def redraw(self):
        """ Redesenha todos os polígonos restantes no canvas."""
        for polygon in self.polygons_aux:
            for i in range(len(polygon)):
                self.canvas.create_oval(polygon[i][0]-3, polygon[i][1]-3, polygon[i][0]+3, polygon[i][1]+3, fill="black")
                self.canvas.create_line(polygon[i], polygon[(i+1) % len(polygon)], fill=self.color2edge, width=4)
                # Repintar a cor do polígono
        self.polygons = self.polygons_aux.copy()
        
        
    def changeEdge_color(self):
        """ Muda a cor da aresta do polígono selecionado."""
        # A ser implementado 
        pass
        
    def fillpoly(self):
        """ Preenche o polígono selecionado."""
        # A ser implementado
        # Variável da cor selecionada:
        self.colorsList[self.selected_polygon] = self.color2paint        
        # Verifica se há um polígono selecionado
        if self.selected_polygon is not None and 0 <= self.selected_polygon < len(self.polygons):
            # Pega o polígono selecionado
            polygon = self.polygons[self.selected_polygon]
            # Desenhar dentro dos limites do polígono
            # Pega os limites do polígono
            x_min = min([point[0] for point in polygon]) 
            x_max = max([point[0] for point in polygon])
            y_min = min([point[1] for point in polygon])
            y_max = max([point[1] for point in polygon])
            # Preenche o polígono
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    if Polygon(polygon).contains(Point(x, y)): # Se o ponto está dentro do polígono
                        self.canvas.create_oval(x, y, x+1, y+1, outline=self.color2paint)
        else:
            messagebox.showwarning("Atenção", "Nenhum polígono selecionado ou seleção inválida.")
                    
if __name__ == "__main__":
    app = PolygonDrawer()
    app.mainloop()

    # Ajustar a lista de cores para redesenhar os polígonos
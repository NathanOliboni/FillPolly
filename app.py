import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, colorchooser
from shapely.geometry import Polygon, Point
import math

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
        
        # CheckBox para pintar a aresta
        self.edge_color_check = ctk.CTkCheckBox(self.main_frame, text="Pintar Aresta", command=self.choose_edge_color)
        self.edge_color_check.grid(row=4, column=0, padx=10, pady=10) 

        # Variáveis para armazenamento
        self.polygons = []  # Lista de polígonos (armazena coordenadas)
        self.current_polygon = []  # Ponto temporário
        self.selected_polygon = None  # Índice do polígono selecionado
        self.current_color = "black"  # Cor padrão para o desenho
        self.color2paint = ""
        self.color2edge = "yellow"
        self.colorsList = [] # Lista para armazenar as cores para redesenhar caso algum seja excluido
        self.edgeColorsList = [] # Lista para armazenar as cores das arestas  
        
        # Adiciona um círculo para exibir a cor selecionada
        self.color_display = self.canvas.create_oval(620, 20, 650, 50, fill=self.current_color, outline="yellow", width=1)
        
        # Eventos do mouse
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Double-Button-1>", self.finish_polygon)  # Fechar polígono com duplo clique
        self.canvas.bind("<Button-3>", self.select_polygon)
        
        # Evento para usuário selecionar o polígono com base em um clique dentro do polígono
        self.canvas.bind("<Button-2>", self.select_polygon)
        
        
    def choose_color(self):
        """ Abre um seletor de cor e atualiza a cor atual e a exibição da cor."""
        color_code = colorchooser.askcolor(title="Escolher Cor")[1]  # Retorna uma tupla (RGB, Hex), pegamos o Hex
        if color_code:
            # self.current_color = color_code # Valor Hex
            self.color2paint = color_code # Valor Hex
            self.canvas.itemconfig(self.color_display, fill=self.current_color)
            
    def choose_edge_color(self):
        """ Abre um seletor de cor e atualiza a cor atual e a exibição da cor."""
        # Verificar se o checkBox está marcado, se sim, muda a cor da aresta, se não define como amarelo
        if self.edge_color_check.get() == 1:
            color_code = colorchooser.askcolor(title="Escolher Cor")[1]
            if color_code:
                self.color2edge = color_code
                self.canvas.itemconfig(self.color_display, fill=self.current_color)
        else:
            self.color2edge = "yellow"
            self.canvas.itemconfig(self.color_display, fill=self.current_color)
            
    def add_point(self, event):
        """ Adiciona um ponto ao polígono atual."""
        x, y = event.x, event.y
        self.current_polygon.append((x, y))
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
        
        # Desenha linhas entre pontos
        if len(self.current_polygon) > 1:
            # A linha deve ser mais grossa para melhor visualização
            self.add_point_line = self.canvas.create_line(self.current_polygon[-2], self.current_polygon[-1], fill=self.color2edge, width=1)
    
    def finish_polygon(self, event=None):
        """ Conclui o desenho de um polígono e o armazena."""
        if len(self.current_polygon) > 2:
            # Fechar o polígono desenhando uma linha do último ponto para o primeiro
            self.add_point_line = self.canvas.create_line(self.current_polygon[-1], self.current_polygon[0], fill=self.color2edge, width=1)
            
            # Adiciona o polígono à lista
            self.polygons.append(self.current_polygon)
            self.colorsList.append('')
            self.edgeColorsList.append(self.color2edge)
            self.current_polygon = []  # Reseta para o próximo desenho
            
            # Atualiza a lista de polígonos no frame lateral
            self.list_polygons()
        else:
            messagebox.showerror("Erro", "Um polígono precisa ter pelo menos 3 pontos.")
        # Printar as coordenadas dos polígonos desenhados
        print(self.polygons)
        print(self.colorsList)
        print(self.edgeColorsList)
    
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
            del self.edgeColorsList[self.selected_polygon]
            
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
        # Redesenha cada polígono com a cor da aresta correspondente
        for index, polygon in enumerate(self.polygons_aux):
            edge_color = self.edgeColorsList[index]  # Cor da aresta para o polígono atual
            for i in range(len(polygon)):
                # Desenha os pontos dos vértices
                self.canvas.create_oval(polygon[i][0] - 3, polygon[i][1] - 3, polygon[i][0] + 3, polygon[i][1] + 3, fill="black")
                # Desenha as arestas com a cor correspondente
                self.canvas.create_line(polygon[i], polygon[(i + 1) % len(polygon)], fill=edge_color, width=1)

        # Copia os polígonos da lista auxiliar
        self.polygons = self.polygons_aux.copy()

        # Redesenha o preenchimento dos polígonos com a cor correta
        for i in range(len(self.polygons)):
            if self.colorsList[i] != '':
                self.selected_polygon = i
                self.color2paint = self.colorsList[i]
                self.fillpoly()
        
    def fillpoly(self):
        """ Preenche o polígono selecionado."""
        # Verifica se há um polígono selecionado
        if self.selected_polygon is None or not (0 <= self.selected_polygon < len(self.polygons)):
            messagebox.showwarning("Atenção", "Nenhum polígono selecionado ou seleção inválida.")
            return

        # Define a cor de preenchimento para o polígono selecionado
        color = self.color2paint
        self.colorsList[self.selected_polygon] = color
        polygon = self.polygons[self.selected_polygon]

        # Encontra ymin e ymax do polígono
        ymin = min(y for x, y in polygon)
        ymax = max(y for x, y in polygon)

        # Cria uma lista para armazenar as interseções para cada scanline
        scanlines = [[] for _ in range(ymin, ymax + 1)]

        # Calcula as interseções para cada aresta do polígono
        for i in range(len(polygon)):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % len(polygon)] # Conecta o último ponto ao primeiro
            print(x1, y1, x2, y2)

            # Ignora arestas horizontais
            if y1 == y2:
                continue

            # Garante que (x1, y1) está abaixo de (x2, y2)
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1

            # Calcula Tx para incremento da coordenada x
            dx = x2 - x1 
            dy = y2 - y1 
            Tx = dx / dy  # Incremento horizontal por unidade vertical

            # Preenche a lista de interseções para cada scanline
            x = x1 # Inicia em x1 e incrementa Tx para cada scanline
            for y in range(y1, y2): # Itera sobre cada scanline
                scanlines[y - ymin].append(x) # Adiciona a interseção na scanline
                x += Tx # Incrementa x para a próxima scanline
                
        print(ymin, ymax)
        print(dx, dy, Tx)
        print("Numero de scanlines:", len(scanlines))
        
        # Preenche as scanlines
        for y, intersections in enumerate(scanlines): # Itera sobre cada scanline
            # Ordena as interseções em ordem crescente
            intersections.sort()

            # Preenche cada par de interseções
            for i in range(0, len(intersections), 2): 
                xini = math.ceil(intersections[i]) # Arredonda para cima
                xfim = math.floor(intersections[i + 1]) # Arredonda para baixo
                
                # Desenha pixels na scanline com a cor de preenchimento
                for x in range(xini, xfim + 1):
                    self.canvas.create_line(x, y + ymin, x + 1, y + ymin, fill=color)
                    print(x, y + ymin)

        
        
        
if __name__ == "__main__":
    app = PolygonDrawer()
    app.mainloop()

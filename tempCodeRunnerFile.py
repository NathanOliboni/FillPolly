        # CheckBox para pintar a aresta
        self.edge_color_check = ctk.CTkCheckBox(self.main_frame, text="Pintar Aresta", command=self.choose_edge_color)
        self.edge_color_check.grid(row=4, column=0, padx=10, pady=10)
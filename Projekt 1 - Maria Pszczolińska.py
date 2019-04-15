import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

#otwarcie plikt do zapisania współrzędnych
plik2= open('Współrzędne punktu przecięcia.txt','w')
szer=40
plik2.write('-' * szer)             
plik2.write("\n| {:^15} | {:^15} |\n".format("Współrzędna X [m]","Współrzędna Y [m]"))
plik2.write('-' * szer)

class AppWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title='Wizualizacja zadania'
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100, 400,300)
        self.show()
        
    def initWidgets(self):
        btn=QPushButton("Rysuj",self)
        btnCol=QPushButton("Kolor punktów",self)
        btnColl=QPushButton("Kolor linii",self)
        xALabel=QLabel("X punktu A",self)
        yALabel=QLabel("Y punktu A",self)
        xBLabel=QLabel("X punktu B",self)
        yBLabel=QLabel("Y punktu B",self)
        xCLabel=QLabel("X punktu C",self)
        yCLabel=QLabel("Y punktu C",self)
        xDLabel=QLabel("X punktu D",self)
        yDLabel=QLabel("Y punktu D",self)
        self.xAEdit=QLineEdit()
        self.yAEdit=QLineEdit()
        self.xBEdit=QLineEdit()
        self.yBEdit=QLineEdit()
        self.xCEdit=QLineEdit()
        self.yCEdit=QLineEdit()
        self.xDEdit=QLineEdit()
        self.yDEdit=QLineEdit()
        resultLabel=QLabel("",self)
        
        #wykres
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        
        grid=QGridLayout()
        grid.addWidget(xALabel, 2, 0)
        grid.addWidget(self.xAEdit, 2, 1)
        grid.addWidget(yALabel, 3, 0)
        grid.addWidget(self.yAEdit, 3, 1)
        grid.addWidget(xBLabel, 4, 0)
        grid.addWidget(self.xBEdit, 4, 1)
        grid.addWidget(yBLabel, 5, 0)
        grid.addWidget(self.yBEdit, 5, 1)
        grid.addWidget(xCLabel, 6, 0)
        grid.addWidget(self.xCEdit, 6, 1)
        grid.addWidget(yCLabel, 7, 0)
        grid.addWidget(self.yCEdit, 7, 1)
        grid.addWidget(xDLabel, 8, 0)
        grid.addWidget(self.xDEdit, 8, 1)
        grid.addWidget(yDLabel, 9, 0)
        grid.addWidget(self.yDEdit, 9, 1)
        grid.addWidget(btn, 10, 0, 1, 2) #rozciąga się na jeden wiersz i dwie kolumny
        grid.addWidget(btnCol, 11, 0, 1, 2)
        grid.addWidget(btnColl, 12, 0, 1, 2)
        grid.addWidget(resultLabel, 12, 0)
        grid.addWidget(self.canvas, 1, 2, -1, -1) #zajmuje miejsce do końca okna
             
        self.setLayout(grid)
        
        btn.clicked.connect(self.oblicz)
        btnCol.clicked.connect(self.zmienKolor)
        btnColl.clicked.connect(self.zmienKolor2)

    def zmienKolor(self):
        color=QColorDialog.getColor()
        if color.isValid():
            print(color.name())
            self.rysuj(col=color.name())
            
    def zmienKolor2(self):
        color2=QColorDialog.getColor()
        if color2.isValid():
            print(color2.name())
            self.rysuj(coll=color2.name())
            
    def oblicz(self):
        self.rysuj()

    def rysuj(self, col='red', coll='blue'):
       
        Xal=self.sprawdzWartosc(self.xAEdit)
        Yal=self.sprawdzWartosc(self.yAEdit)
        Xbl=self.sprawdzWartosc(self.xBEdit)
        Ybl=self.sprawdzWartosc(self.yBEdit)
        Xcl=self.sprawdzWartosc(self.xCEdit)
        Ycl=self.sprawdzWartosc(self.yCEdit)
        Xdl=self.sprawdzWartosc(self.xDEdit)
        Ydl=self.sprawdzWartosc(self.yDEdit)
        if (Xal is not None) and (Yal is not None) and (Xbl is not None) and (Ybl is not None) and (Xcl is not None) and (Ycl is not None) and (Xdl is not None) and (Ydl is not None):
            #czyszczenie wykresu
            self.figure.clear()
            ax=self.figure.add_subplot(111) #dodajemy siatkę 1 na 1 na 1
            
            #obliczenie wspolrzednych punktu P
            while (Xbl-Xal)*(Ydl-Ycl)-(Ybl-Yal)*(Xdl-Xcl)!=0:
                t1=((Xcl-Xal)*(Ydl-Ycl)-(Ycl-Yal)*(Xdl-Xcl))/((Xbl-Xal)*(Ydl-Ycl)-(Ybl-Yal)*(Xdl-Xcl))
                break
            while (Xbl-Xal)*(Ydl-Ycl)-(Ybl-Yal)*(Xdl-Xcl)!=0:
                t2=((Xcl-Xal)*(Ybl-Yal)-(Ycl-Yal)*(Xbl-Xal))/((Xbl-Xal)*(Ydl-Ycl)-(Ybl-Yal)*(Xdl-Xcl))
                break
            Xp=Xal+t1*(Xbl-Xal)
            Yp=Yal+t1*(Ybl-Yal)
            
            #współrzędne punktów
            yy=[Yal, Ybl, Ycl, Ydl, Yp]
            xx=[Xal, Xbl, Xcl, Xdl, Xp]
            xAB=[Xal, Xbl]
            yAB=[Yal, Ybl]
            xCD=[Xcl, Xdl]
            yCD=[Ycl, Ydl]
            
            xAP=[Xal,Xp]
            yAP=[Yal,Yp]
            xBP=[Xbl,Xp]
            yBP=[Ybl,Yp]
            xCP=[Xcl,Xp]
            yCP=[Ycl,Yp]
            xDP=[Xdl,Xp]
            yDP=[Ydl,Yp]
            
            nn=['A', 'B', 'C', 'D', 'P']
            
            #rysowanie punktów i linii ich łączących
            plt.scatter(xx,yy, color=col, marker='o')
            plt.plot(xAB,yAB, color=coll, linewidth=0.5)
            plt.plot(xCD,yCD, color=coll, linewidth=0.5)
            for i, txt in enumerate(nn):
                ax.annotate(txt, (xx[i], yy[i]))
                
            print('Współrzędna X punktu przecięcia P:','%.3f' % Xp)
            print('Współrzędna Y punktu przecięcia P:','%.3f' % Yp)
            
            #wiadomosc o położeniu punktu względem odcinków oraz ewentualne rysowanie linii, jeżeli punkt P znajduje się na przedłużeniu
            if (Xbl-Xal)*(Ydl-Ycl)-(Ybl-Yal)*(Xdl-Xcl)==0:
                print('Proste równoległe, brak punktu przecięcia')
            else:
                if 0<=t1<=1 and 0<=t2<=1:
                    print('Punkt leży na przecięciu odcinków')
                elif t1<0 and 0<=t2<=1:
                    print('Punkt leży na przedłużeniu odcinka AB')
                    plt.plot(xAP,yAP, color=coll,linestyle='-.', linewidth=0.5)
                elif t1>1 and 0<=t2<=1:
                    print('Punkt leży na przedłużeniu odcinka AB')
                    plt.plot(xBP,yBP, color=coll,linestyle='-.', linewidth=0.5)
                elif t2<0 and 0<=t1<=1:
                    print('Punkt leży na przedłużeniu odcinka CD')
                    plt.plot(xCP,yCP, color=coll,linestyle='-.', linewidth=0.5)
                elif t2>1 and 0<=t1<=1:
                    print('Punkt leży na przedłużeniu odcinka CD')
                    plt.plot(xDP,yDP, color=coll,linestyle='-.', linewidth=0.5)
                    
                elif t1<0 and t2<0:
                    print('Punkt leży na przedłużeniu obu odcinków')
                    plt.plot(xAP,yAP, color=coll,linestyle='-.', linewidth=0.5)
                    plt.plot(xCP,yCP, color=coll,linestyle='-.', linewidth=0.5)
                elif t1<0 and t2>1:
                    print('Punkt leży na przedłużeniu obu odcinków')
                    plt.plot(xAP,yAP, color=coll,linestyle='-.', linewidth=0.5)
                    plt.plot(xDP,yDP, color=coll,linestyle='-.', linewidth=0.5)
                elif t1>1 and t2<0:
                    print('Punkt leży na przedłużeniu obu odcinków')
                    plt.plot(xBP,yBP, color=coll,linestyle='-.', linewidth=0.5)
                    plt.plot(xCP,yCP, color=coll,linestyle='-.', linewidth=0.5)
                elif t1>1 and t2>1:
                    print('Punkt leży na przedłużeniu obu odcinków')
                    plt.plot(xBP,yBP, color=coll,linestyle='-.', linewidth=0.5)
                    plt.plot(xDP,yDP, color=coll,linestyle='-.', linewidth=0.5)
                    
            #odswieżenie wykresu
            self.canvas.draw()
            
            #zapisane wspolrzednych punktu P do pliku tekstowego            
            plik2.write('\n| {:^18}| {:^18}|'.format('%.3f' %Xp,'%.3f' %Yp))
            
    def sprawdzWartosc(self, element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            element.setFocus()
            return None
        
def main():
    app=QApplication(sys.argv)
    window=AppWindow()
    app.exec_()
    
if __name__=='__main__':
    main()

#zamkniecie pliku z zapisanymi danymi    
plik2.close()   
    
#KOMPONENTY
#po kliknieciu licz bedzie wyznaczana wspolrzedna punktu P
#po kliknieciu rysuj bedzie rysowany wykres
#albo w QtDesigner albo się męczyć - JAK WOLISZ
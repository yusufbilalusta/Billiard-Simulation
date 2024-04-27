import numpy as np
import matplotlib.pyplot as plt
import json

class Base:
    #Bu class Base durumunu temsil eder. Intermediate ve Advanced durumlar bu classı miras alır
    def __init__(self):

        with open('Initial-State.json', 'r') as file:
            info = json.load(file)

        self.table_width = info[0]["table"]["width"]
        self.table_height = info[0]["table"]["height"]
        self.count_of_balls = len(info[0]["balls"])
        self.positions_of_balls = []
        self.velocities_of_balls = []
        for ball in info[0]["balls"]:
            position = [ball["position"]["x"], ball["position"]["y"]]
            velocity = [ball["velocity"]["x"], ball["velocity"]["y"]]
            self.positions_of_balls.append(position)
            self.velocities_of_balls.append(velocity)

        self.positions_of_balls = np.array(self.positions_of_balls)
        self.velocities_of_balls = np.array(self.velocities_of_balls)
        self.radius_of_balls = np.full(self.count_of_balls,info[0]["ball"]["radius"])
        self.deacceleration = np.full((self.count_of_balls,2),info[0]["table"]["deacceleration"])

        time_list = np.round(np.random.rand(6) * 10, 1)
        with open("snapshot-times.txt", "w") as file:
            for i in time_list:
                file.write(str(i) + " ")



    def Move_balls(self,duration=1):
        self.new_positions = self.positions_of_balls + self.velocities_of_balls*duration - (self.deacceleration*(duration**2))/2
        #Toplarin yaricaplari masa kenarlarina dreadnduktan sonra o kenarı gecemez
        for i in range(self.count_of_balls):
            if self.new_positions[i,0] + self.radius_of_balls[i] > self.table_width:
                self.new_positions[i,0] = self.table_width - self.radius_of_balls[i]
            elif self.new_positions[i,0] - self.radius_of_balls[i] < 0:
                self.new_positions[i,0] = 0 + self.radius_of_balls[i]
            if self.new_positions[i,1] + self.radius_of_balls[i] > self.table_height:
                self.new_positions[i,1] = self.table_height - self.radius_of_balls[i]
            elif self.new_positions[i,1] - self.radius_of_balls[i] <0:
                self.new_positions[i,1] = 0 + self.radius_of_balls[i]
        self.positions_of_balls = self.new_positions

    def Simulation(self,limit = 100,duration = 0.1,name = "BaseOutput"):
        self.outputList = []
        self.limit = limit #Toplam adim numbersi
        self.duration = duration #Bir adimin durationsi
        self.name= name
        lines = self.read()
        numbers = []
        for line in lines:
            # linedaki numbersı boşluklara göre ayır
            numList = line.strip().split()
            for num_str in numList:
                numbers.append(float(num_str))
        for i in range(self.limit):
            plt.clf() #Dongunun her adiminda onceki cizimi temizleriz
            plt.xlim(0,self.table_width) #Grafigin x ve y degerleri 0 dan masa nin en ve boy degerlerine kadar olur
            plt.ylim(0,self.table_height)
            plt.title("Top Pozisyonlari")
            plt.gca().set_aspect(1, adjustable='box')
            self.Move_balls(duration)
            for j in range(self.count_of_balls):
                daire = plt.Circle((self.positions_of_balls[j,0],self.positions_of_balls[j,1]),self.radius_of_balls[j],color='green',alpha = 0.5)
                if (self.linear_search(numbers,i*duration)):
                    self.outputList.append({
                        "time": i*duration,
                        "id" : j,
                        "X position": self.positions_of_balls[j, 0],
                        "Y Position": self.positions_of_balls[j, 1]
                    })

                plt.gca().add_patch(daire)
            plt.pause(0.05)
            plt.draw()
        with open(f"{name}.json", "w") as file:
            json.dump(self.outputList, file)
        plt.show()


    def read(self):
        try:
            with open("snapshot-times.txt","r") as file:
                return file.readlines()
        except FileNotFoundError:
            print("file Bulunamadi")

    def linear_search(self,arr, x):
        number = round(x,1)
        h= str(number)
        for i in range(len(arr)):
            if str(arr[i]) == h:
                return True
        return False


class Intermediate(Base):
    def Move_balls(self,duration=0.1):
        self.new_positions = self.positions_of_balls + duration*self.velocities_of_balls - (self.deacceleration*(duration**2))/2
        for i in range(self.count_of_balls):
            if self.new_positions[i,0] + self.radius_of_balls[i] > self.table_width:
                self.new_positions[i,0] = self.table_width - self.radius_of_balls[i]
                self.velocities_of_balls[i,0]*=(-1)
            elif self.new_positions[i,0] - self.radius_of_balls[i] < 0:
                self.new_positions[i,0] = 0 + self.radius_of_balls[i]
                self.velocities_of_balls[i,0]*=-1
            if self.new_positions[i,1] + self.radius_of_balls[i] > self.table_height:
                self.new_positions[i,1] = self.table_height - self.radius_of_balls[i]
                self.velocities_of_balls[i,1] *=-1
            elif self.new_positions[i,1] - self.radius_of_balls[i] < 0:
                self.new_positions[i,1] = 0 + self.radius_of_balls[i]
                self.velocities_of_balls[i,1] *=-1
        self.positions_of_balls = self.new_positions


    def Simulation(self,limit = 300,duration = 0.1,name = "IntermediateOutput"):#Kisaltma Yöntemini arastir gereksiz gibi duruyor
        super().Simulation(limit=limit,duration=duration,name=name)

class Advanced(Intermediate):
    def Distance(self,i,j):
        dist_x = self.positions_of_balls[j, 0] - self.positions_of_balls[i, 0]
        dist_y = self.positions_of_balls[j, 1] - self.positions_of_balls[i, 1]
        dist = np.sqrt(dist_x ** 2 + dist_y ** 2)
        summ =self.radius_of_balls[j] + self.radius_of_balls[i]
        return dist, summ


    def Move_balls(self,duration=1):
        super().Move_balls(duration)
        #Intermediate deki duvar carpismasina ek olarak toplarda carpistirilir
        #Toplarin carpisma kontrolu icin x ve y degerleri arasindaki farklardan hipotenus teoremi kullanilir.
        for i in range(self.count_of_balls):
            for j in range(i+1,self.count_of_balls):
                dist,summ = self.Distance(i,j)
                if dist < summ:
                    #Toplarin pozisyonlari yendien ayarlandiktan sonra momentum formulu uygulanir
                    m1 = self.radius_of_balls[i]**2 #m = kutle
                    m2 = self.radius_of_balls[j]**2
                    v1 = self.velocities_of_balls[i] #v = hiz
                    v2 = self.velocities_of_balls[j]
                    #https://www.geeksforgeeks.org/elastic-collision-formula/
                    #Elastik Carpisma Formulu asagidaki gibidir
                    new_v1 = ((m1 - m2)*v1 + 2*m2*v2) / (m1 + m2)
                    new_v2 = ((m2 - m1)*v2 + 2*m1*v1) / (m1 + m2)
                    self.velocities_of_balls[i] = new_v1
                    self.velocities_of_balls[j] = new_v2

    def Simulation(self,limit = 300,duration = 0.1,name = "AdvancedOutput"):#Kisaltma Yöntemini arastir gereksiz gibi duruyor
        super().Simulation(limit=limit, duration=duration, name=name)


class Expert(Advanced):
    def __init__(self):
        self.table_width = 10
        self.table_height = 10
        self.count_of_balls = 10
        self.positions_of_balls = np.random.rand(self.count_of_balls,2)*[self.table_width,self.table_height] #Hem x hem y düzleminde 0 ile 1 arasında random number üretilir
                                                                                        #Bu numbersın maks değeri masanin en ve boyuna esit olacaktir
                                                                                        #Bu sayede hic bir topun baslangic adresi masanin disinda olamaz

        self.radius_of_balls = np.random.rand(self.count_of_balls)*0.6 #En buyuk top yaricapi 0.6 olucak sekilde sinirlandirildi
        self.velocities_of_balls = np.random.randn(self.count_of_balls,2) #Topların hızları -1 ile +1 arasında olacak sekilde sınırlandırıldı
        self.baslangic_konumlari_list = []
        self.deacceleration = np.full((self.count_of_balls,2), 0.1)
        for i in range(self.count_of_balls):
            self.baslangic_konumlari_list.append(
                {"Id: ": i,
                 "X position: ":self.positions_of_balls[i,0],
                 "Y position: ":self.positions_of_balls[i,1]})
        with open("Initial-State-Expert.json","w") as file:
            json.dump(self.baslangic_konumlari_list,file)

        time_list = np.round(np.random.rand(6) * 10, 1)
        with open("snapshot-times.txt", "w") as file:
            for i in time_list:
                file.write(str(i) + " ")

        #Toplar birbirleriyle carpisacagi icin baslangic konumlari onemlidir
        #Eger birbirleri ile cakisik bicimde dogarlarsa durationkli olarak cakismaya devam ederler
        #Bunu onlemek icin baslangic durumu kontrol edilir.
        for i in range(self.count_of_balls):
            for j in range(i+1,self.count_of_balls):
                dist,summ = self.Distance(i,j)
                if dist < summ:
                    while(dist < summ):
                        self.positions_of_balls[i] = np.random.rand(1, 2) * [self.table_width,self.table_height]
                        self.radius_of_balls[i] = np.random.rand() * 0.6  # En buyuk top yaricapi 0.6 olucak sekilde sinirlandirildi

    def Simulation(self,limit = 500,duration = 0.1,name = "ExpertOutput"):#Kisaltma Yöntemini arastir gereksiz gibi duruyor
        super().Simulation(limit=limit, duration=duration, name=name)


pool = Expert()
pool.Simulation()
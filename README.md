# (COVIS) COVID VISUALIZER V 1.0

The project uses Python scripts and datasets, to creates the correct files to visualize Covid data in a Google Data Studio  Tableau or Power BI dashboard and produce some interactive graphics in .html .svg and .pndg to use wherever you want.

## How does it work?
The Scripts follows a structure to produce the correct results:
 * `Covid_template.xslx` This file contains preloaded COVID data cases by country from the beginning until October 2020. it is the template where new data should be added according to the date.
 * `Covid_confirmed.csv` Alternatively, you can choose to use a .csv file to load the data but it must keep the structure indicated in this file
 * `COVIS_V1_0.py` Python Script to process, clean the data and produce the graphics and datasets to visualize in a third party platform.

This is the first version and there are many things to improve that could be added to the script, feel free to contribute if you wish.

## User guide 

### **1. Updating data :**
  Once you have downloaded the code, put the COVIS folder in the place you prefer, open it and go to the `input` folder and choose a file to update `Covid_template.xslx` or `Covid_confirmed.csv` you can update in excel or in the text editor that you prefer and create a date column to the end of the table in this way -> `7/26/21`.
  You can create as many date columns as you like, don't forget to keep the structure
 
#### **1.1. Adding data:** 
  Fill each row with daily Covid cases by country for a specific date, if you don't have the data for a specific country, put the value of the previous date in the row and save changes.

### **2. The Script `COVIS_V1_0.py`**
Once you have the dataset file ready you can start with the processing scripts.
   
##### **2.1 Requirements:**
  This script works using the Python language and some Python libraries to clean and process data, so this software needs to be installed. If you have already installed this software, you can skip this step.

  + Python:
    You can install python directly from here:

    + Oficial version download: https://www.python.org/downloads/
    
   + Python libraries:
    Go to your prefer IDE (Pycharm, VS code) and install the libraries using pip method, otherwise use conda method.

     ```
        shell> python -m pip install --upgrade pip
        pip install pandas
        pip install matplotlib
        pip install folium
     ``` 
  Wait for the processes to finish and close the terminal to finish


#### **2.2 Setting the script:** 
  + Open the script and set your default values in the code:
    + Path_ : Where you put the `COVIS` folder, do noy forget to finish with / in the path, you can change it by console
    + country_in : Default country to run the code, you can change it by console
    + end_date_in : Last date from covid cases you add
    + start_date_in : First date from covid cases, do not modify it but iy you want to do it change it in this line

  + If you don't put the default path the script will show you an error

  Find the code in line 12 in COVIS script.
  ```
  # ------------------------------------------------------
  # Default config
  # -----------------------------------------------------
    # put the default path here
  --> path_ = "E:/Desktop/.../"

    # put last date from new data for instance "2021-09-23"  here
  --> end_date_in = "2020-10-17" 

    # if you change the start date for any reason put it here
  --> start_date_in = "2020-01-22"

    # if you want to change the default country put ir here
  --> country_in = "Colombia"  
  ```
  + Set the file extension from which the data will be read .csv .xlsx by
  turning on or off the lines. I recomend you to use the .xlsx extension it is easier to update but if you use the .csv extension do not forget to change the delimiter for the correct one after edit the file (In excel maybe you should used delimiter= ' ; ' )

  Find the code in line 39 in COVIS script.

  ```
  # ----------------------------------------------------------
  # default file type config
  # ----------------------------------------------------------
  try:
      path = input("seleccion al ruta o ENTER para ruta default: ")
  --> # df = pd.read_csv(f'{path}COVIS/input/Covid_confirmed.csv', delimiter=',') # csv
  -->   df = pd.read_excel(f'{path}COVIS/input/Covid_template.xlsx')  # xlsx
      print("Ruta cargada leyendo datoos...\n")
  except:
      path = path_
      # default path
  --> # df = pd.read_csv(f'{path}COVIS/input/Covid_confirmed.csv', delimiter=',') # csv
  -->   df = pd.read_excel(f'{path}COVIS/input/Covid_template.xlsx')  # xlsx
      print("Ruta default cargada leyendo datoos...\n")
  ```

  + You do not need to change anything else in the script, save changes and run it

#### **3. Running the Script:** 
  + Once you have finished all the configurations, run the script and wait until the process is finished, you will be able to see in the console the results that it is producing. Something like that
  
  
  ```
    >>> Cargando datos...

    Ruta default cargada leyendo datoos...

    >>> Creando dataframe global...

        Province/State Country/Region  ...  10/16/20  10/17/20
    0              NaN    Afghanistan  ...     40073     40141
    1              NaN        Albania  ...     16501     16774
    ..             ...            ...  ...       ...       ...
    265            NaN         Zambia  ...     15659     15789
    266            NaN       Zimbabwe  ...      8099      8110

    [267 rows x 274 columns]

    >>> Creando dataframe casos mensuales por pais...
  ```

+ Within the Script, data entry will be requested, it will ask you if you want to load the data from a different route and you can put a diferent path by console as before if not, you can simply give ENTER and it will load the default route, besides it will be requested to select the graphs date, as well as the country for the visualizations, if you do not want to put the information you can press ENTER and the Script will load the data by default. Follow the script instructions to avoid errors in the code

+ Image, Daily cases by country example

    ![Daily cases by country](https://github.com/HARDROCO/-COVIS-COVID_VISUALIZER/blob/main/output/Colombia_dailycases_CV19_2020-01-22_2020-10-17.png)

+ Interactive map, Total cases by country

    ![Total cases by country](https://github.com/HARDROCO/-COVIS-COVID_VISUALIZER/blob/main/images/map_total_cas.PNG)

+ When the process finishes
  
  ```
    Fin del análisis por ahora :) ...
    ------------------------------------------------------------
    ------------------------------------------------------------
      *Script made by Hardroco | 2021 - MIT license.
    ------------------------------------------------------------
    ------------------------------------------------------------
  ```    
+ Go to the `output` folder and there you will find the following files:

  + Datasets to use in GDS, Tableau, Power Bi
    + dailycases_CV19_by_country_large .csv and .xlsx
    + Country_dailycases_startdate_enddate .csv and .xlsx
    + monthcases_CV19_by_country_ .csv and .xlsx
    + totalcases_country_date_ .csv and .xlsx
  + Images to use wherever you want
    + map_totalcases_country_date_  ---> interactive image .html
    + country_dailycases_CV19_startdate_enddate ---> vector image .svg  and .png

Check the output folder to find some examples.

#### **4. Visualizing data in Google data studio**

+ Once the script has finished the process, you can go to the google data studio link where the visualization dashboard for daily covid cases by country will be found.
+ The dashboard is public, you can share it, download it and make a copy to your account to load the new data generated by the script(check the images folder to see an example)
+ Keep the names of the files generated by the script and load them as required by the graphics in each panel.
+ You will need the following files to use the dashboard
  + monthcases_CV19_by_country_2020.csv
  + dailycases_CV19_by_country_large.csv

+ Also, you could use the .xlxs files but you will need to put them into your google account and in a google sheets 

  ![copy Dashboard](https://github.com/HARDROCO/-COVIS-COVID_VISUALIZER/blob/main/images/covis_m_copy.PNG)


  + Link : [Dashboard GDS, Covid daily cases](https://datastudio.google.com/s/mjWSAdwfgZ4)

+ Dashboard Example

  ![Dashboard Example](https://github.com/HARDROCO/-COVIS-COVID_VISUALIZER/blob/main/images/dashboard_gds.PNG)


That's all !


License
---------------
MIT 

Enjoy
---------------
If this tool has been useful for you, feel free to thank me in your program code or in the comment section.

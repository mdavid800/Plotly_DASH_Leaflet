#Uploaded to AzureDevops test
#Upload to GIT test
#%%
#Import dash components
import dash  # (version 1.12.0) pip install dash
from dash import dcc,html,dash_table,callback_context
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
from dash.dependencies import Input, Output,State
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

#import other libraries
import pandas as pd
from pyproj import Proj, transform
import geopandas as gpd # you need to pip install gdal then fiona .whl files first.
import json,requests
import leafmap.plotlymap as leafmap
from PIL import Image;


import plotly.io as pio
pio.renderers.default='browser'
#pycharm test
import os

#set style to DBC FLATLY
app = Dash(__name__)

#%%
cwd = os.getcwd() #This is the current working directory will be the plotlytests project folder, we have a Resource Files folder within the project for shared sample files
resourceFilesFolderPath = cwd + "\\ResourceFiles"
popfile="popsgrn.csv"
SSE_LOGO="SSE_Renewables_Logo_Strap_RGB.png"

popfilepath = os.path.join(resourceFilesFolderPath, popfile)
SSE_LOGOpath = os.path.join(resourceFilesFolderPath, SSE_LOGO)
# Import Sample Data from local file - columns are "TurbineID", "Easting(m)", "Northing(m)","Elevation","PoP", "RotorDiameter"
pop_df = pd.read_csv(popfilepath) 
pop_df['id'] = pop_df['TurbineID']
pop_df.set_index('id', inplace=True, drop=False)

#Load in separate geojson from local file for site boundary 
sgrnGeoJsonPath =os.path.join(resourceFilesFolderPath, "seagreen_json.geojson")
with open(sgrnGeoJsonPath) as json_data:
  js = json.loads(json_data.read())

alphaBravo_gdf = gpd.GeoDataFrame.from_features(js)
alphaBravo_gdf = alphaBravo_gdf.loc[~alphaBravo_gdf.geometry.is_empty]

#transform data to correct CRS (from WRG 84 Zone 30N (espg:32630) to Lat/Lon(espg:4326) and add back to data frame
inProj, outProj = Proj(init='epsg:32630'), Proj(init='epsg:4326')
pop_df['x2'], pop_df['y2'] = transform(inProj, outProj, pop_df['Easting (m)'].tolist(), pop_df['Northing (m)'].tolist())

#%%
#Load images 
SSELogoImg= Image.open(SSE_LOGOpath)

# Page Header - This code sets up the Page Header , which will be used in the layout section later . I have used Dash Mantine Components for this header. 
# I have wrapped in a function to allow for it to be repeatable - maybe this should site external from code and be edited separately 
def page_header():
    return dmc.Header(
        height=70,
        fixed=True,
        p="md",
        children=[
            dmc.Group(
                position="apart", 
                style={"marginLeft": 20, "marginRight": 20},
                children=[
                    dmc.Group(
                        [
                            
                            dcc.Link(
                                #dmc.Text("SSE Renewables"),
                                dmc.Image(src=SSELogoImg, width=150),
                                href="https://www.sserenewables.com",
                                style={"textDecoration": "none"},
                            ), 
                        ]
                    ),
                    #set up some buttons these are just examples but i like them . Thinking we could have HELP Page or Yammer page set up like this
                    dmc.Group(
                        position="right",
                        children=[
                            html.A(
                                dmc.Button(
                                    dmc.Text(
                                        "Source Code",
                                        color="dark",
                                        weight="lighter",
                                        size="sm",
                                    ),
                                    radius="xl",
                                    variant="light",
                                    color="gray",
                                    rightIcon=[
                                        DashIconify(
                                            icon="cib:azure-devops",
                                            color="black",
                                            width=20,
                                        )
                                    ],
                                ),
                                href="https://vsosse.visualstudio.com/",
                                className="hide-sm",
                            ),
                            html.A(
                                dmc.Button(
                                    dmc.Text(
                                        "Teams",
                                        color="dark",
                                        weight="lighter",
                                        size="sm",
                                    ),
                                    radius="xl",
                                    variant="light",
                                    color="gray",
                                    rightIcon=[
                                        DashIconify(
                                            icon="bxl:microsoft-teams",
                                            color="black",
                                            width=20,
                                        )
                                    ],
                                ),
                                href="https://teams.microsoft.com/l/channel/19%3a6a676d4a99814c16ab2bcc7b37164d0e%40thread.skype/Coding%2520HELP?groupId=319b4bb5-e814-4382-b108-825e09026c0c&tenantId=953b0f83-1ce6-45c3-82c9-1d847e372339",
                                className="hide-sm",
                            ),
                            # this search bar doesn't actually do anything , i just like it in . I figure we could turn it into the help section in the long run 
                            dmc.Select(
                            style={"width": 300},
                            placeholder="Search Help",
                            searchable=True,
                            icon=[DashIconify(icon="radix-icons:magnifying-glass")],
                            data=["Test1", "Test2", "Test3"],
                        ),
                        ],
                    ),
                ],
            )
        ],
    )

#Side Nav - This code Sets up the side nav for the page. The side nav at present doesn't actually link to anything but just shows proof of concept
def side_nav():
   # sections = defaultdict(list)

    #leaving this code in but commenting out , this is some of the boiler plate that will allow us to do multipage apps. 
    # for entry in dash.page_registry.values():
    #     label = entry["module"].split(".")[1]
    #     label = (" ".join(label.split("-"))).title()
    #     sections[label].append((entry["name"], entry["path"]))

    #QTools = dmc.Text("QuickTools", color="light"),

    children = [dmc.Accordion(
    [
        dmc.AccordionItem(
            icon=[DashIconify(icon="carbon:tool-kit", color="#f6b21b")],
            label="QuickTools",
            children=["I-EPE"],
        ),
        dmc.AccordionItem(
            icon=[DashIconify(icon="akar-icons:check-in", color="#f6b21b")],
            label="KITE",
            children=["Item 2"],
        ),
        dmc.AccordionItem(
            icon=[DashIconify(icon="ant-design:check-circle-outlined", color="#f6b21b")],
            label=[ "LCoE"],
            children=["Item 3"],
        ),
    ],
    disableIconRotation=True,
)]
    #The below code allows for multipage apps but i am commenting out just now  as we dont have any other apps / pages to add in
    # for section, pages in sorted(sections.items(), reverse=True):
    #     if section not in ["Home"]:
    #         component = dmc.Accordion(
    #             state={"0": True},
    #             iconPosition="right",
    #             icon=[DashIconify(icon="radix-icons:chevron-down")],
    #             children=[
    #                 dmc.AccordionItem(
    #                     label=section,
    #                     children=[
    #                         dmc.Group(
    #                             direction="column",
    #                             spacing="xs",
    #                             children=[
    #                                 dcc.Link(
    #                                     dmc.Text(name, size="sm", color="gray"),
    #                                     href=path,
    #                                     id=name,
    #                                     style={"textDecoration": "none"},
    #                                 )
    #                                 for name, path in pages
    #                             ],
    #                         )
    #                     ],
    #                 )
    #             ],
    #         )
    #         children.append(component)

    return dmc.Navbar(
        id="components-navbar",
        fixed=True,
        position={"top": 70,"left":0},
        style={"backgroundColor": "#002d72","color": "#FFFFFF"},
        width={"base": 250},
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                children=children,
            )
        ],
    )


# set out App layout
#define style "pre" for use by app
styles = {
    'pre': {
        'border': 'thin purple solid',
        'overflowX': 'scroll'
    }
}


# pcDatatable =  dash_table.DataTable(
#         id='turbine-data-table',
#        #columns=[{"name": i, "id": i} for i in df_TurbineData.columns],
#         data=[],
#     )

app.layout = dmc.MantineProvider(
    

        theme={"colorScheme": "light",

        #SSE Colours added to theme

        "colors":{
            "SSE_Blue":["#002d72"],
            "SSE_White":["#ffffff"],
            "SSE_Teal":["#0097a9"],
            "SSE_LightBlue":["#a2b2c8"],
            "SSE_Amber":["#f6b21b"],
            "SSE_Mint":["#6bcaba"],
            "SSE_Grey":["#425563"],
                    },
            },
        styles = {"Accordion":{"label":{"color": "#ffffff"}}},
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.NotificationsProvider(
                [
                    dmc.Container(
                        
                        children=[
                            page_header(),
                            side_nav(),
                            #second container allows for content to be positioned around the rest if the webpage (i.e. sidebar , navbar etc)
                            dmc.Container(
                                dmc.Grid([
                                    
                                   
                                    #Mantine Grid moves components onto new row once 12 columns are used , so this moves onto new row. 
                                    #Changed date picker to Mantine Date Picker - sexy date picker 
                                    
                                    dmc.Col(dmc.Button("submit",id='btn-nclicks-1', fullWidth=True, variant="outline"),span = 12),

                                    html.Br(),

                                    dmc.Col(dmc.Text("Click to display map"),span=12),

                                    html.Br(),
                                    
                                    dmc.Col( dcc.Graph(id='POP_Map', 
                                                        config={'displayModeBar': True},
                                                        style ={"height": "600px"}
                                                         #figure=turbineDataFigure we don't have any data on first load and will pass in a figure later
                                                        ),span=12),

                                    
                                    

                                ],justify="space-around"),
                                style={"marginLeft": 170,"marginTop": 10, "backgroundColor": "#fafafa"},
                                fluid=True,
                                p="lg",
                                id="main-content",
                                #children=children,     
                            ),
                    ],
                        fluid=True,
                        p="sm",
                        style={"marginLeft": 150, "marginRight": 30, "marginTop": 50}),
                ]),
        ])
        
        


  

#%%
#app call back Output is figure, inout is click button 
@app.callback(
Output(component_id='POP_Map', component_property='figure'),
Input(component_id='btn-nclicks-1', component_property='n_clicks'),

 prevent_initial_call=True
)
# if button clicked then plot figures , as per function convention btn-nclicks-1 is changed to load_POP

def update_pop_graph_and_table(load_POP):

            fig = leafmap.Map()
            fig = leafmap.Map(center=(40, -100), zoom=3, height=300)
            fig.add_controls('drawline')
            fig.add_basemap()
            #.add_heatmap_demo()
            #fig.add_scatter_plot_demo()
            #fig.show
        
            #return figure to output
            return fig 


if __name__ == '__main__':
    app.run_server(debug=True)
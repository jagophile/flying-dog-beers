import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import plotly.tools as tls
from matplotlib.figure import Figure

import pickle,os

import time

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Plotting Spectral with AtomDB'
tabtitle='Plotting Spectral with AtomDB'
#myheading='Flying Dog Beers'
#label1='IBU'
#label2='ABV'
githublink='https://github.com/jagophile/flying-dog-beers'
#sourceurl='https://www.flyingdog.com/beers/'
data = 'response'

########### Set up the chart

#--data = pickle.load(open('response/precalc_spec_acistest.pkl', 'rb'))
#--
#--binedges = data['ebins']
#--displayspec = np.append(1e-40, data[30])
#--
#--trace1 = go.Scatter(x=binedges, y=displayspec,
#--            line=dict(
#--                shape = 'hv',
#--                color = '#9467bd'
#--            ),
#--            mode='lines',
#--            name='Plot')
#--#bitterness = go.Bar(
#--#    x=beers,
#--#    y=ibu_values,
#--#    name=label1,
#--#    marker={'color':color1}
#--#)
#--#alcohol = go.Bar(
#--#    x=beers,
#--#    y=abv_values,
#--#    name=label2,
#--#    marker={'color':color2}
#--#)
#--
#--#beer_data = [bitterness, alcohol]
#--#beer_layout = go.Layout(
#--#    barmode='group',
#--#    title =
#--
#--xaxis='keV'
#--xaxis_type='Linear'
#--yaxis_type='Linear'
#--
#--ret = {
#--     'data': [trace1],
#--    'layout': go.Layout(
#--            xaxis={'title': xaxis, 'type': 'linear' if xaxis_type == 'Linear' else 'log'},
#--            yaxis={
#--                'title': 'Emissivity*Aeff (ph cm^5 s^-1 bin^-1)',
#--                'type': 'linear' if yaxis_type == 'Linear' else 'log'
#--                },
#--            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#--            #legend={'x': 0, 'y': 1},
#--            hovermode='closest',
#--            uirevision = True,
#--            showlegend=False,
#--        )
#--    }
#--
#--

#beer_fig = go.Figure(data=ret['data'], layout=ret['layout'])


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

HC_IN_KEV_A = 12.398425

def Ztoelsymb(Z) :
  """
  Returns element symbol of element with nuclear charge Z.

  PARAMETERS
  ----------
  Z  - nuclear charge of element (e.g. 6 for carbon)

  RETURNS
  -------
  element symbol (e.g. "C" for carbon)

  Version 0.1 28 July 2009
  Adam Foster
  """

  elsymb=('H' , 'He', 'Li', 'Be', 'B' , 'C' , 'N' , 'O' , 'F' , 'Ne',
          'Na', 'Mg', 'Al', 'Si', 'P' , 'S' , 'Cl', 'Ar', 'K' , 'Ca',
          'Sc', 'Ti', 'V' , 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
          'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y' , 'Zr',
          'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
          'Sb', 'Te', 'I ', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
          'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
          'Lu', 'Hf', 'Ta', 'W' , 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
          'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
          'Pa', 'U')

  if Z < 1 :
      print("Z must be between 1 and 92. You have given Z= " + repr(z0))
      ret=-1
  elif Z > 92 :
      print("Z must be between 1 and 92. You have given Z= " + repr(z0))
      ret=-1
  else :
      ret=elsymb[Z-1]
  return ret

def int2roman(number):

    numerals = { 1   : "I" , 4   : "IV", 5    : "V" , 9   : "IX", 10  : "X" ,
                 40  : "XL", 50  : "L" , 90   : "XC", 100 : "C" , 400 : "CD",
                 500 : "D" , 900 : "CM", 1000 : "M" }
    result = ""

    for value, numeral in sorted(list(numerals.items()), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result

def spectroscopic_name(Z,z1) :
  """
  Converts Z,z1 to spectroscopic name, e.g. 6,5 to "C V"

  Parameters
  ----------

  Z : int
    nuclear charge (e.g. 6 for C)
  z1 : int
    ion charge +1 (e.g. 5 for C4+)

  Returns
  -------
  str
    spectroscopic symbol for ion (e.g. "C V" for C+4)

  """
#
#  Version 0.1 28 July 2009
#  Adam Foster
#
    # get element symbol
  elsymb = Ztoelsymb(Z)

    # convert z1 to spectroscopic

  roman = int2roman(z1)
  ret = elsymb + ' ' + roman

  return ret


# print the filename

#print("Pyatomdb file: ", pyatomdb.__file__)

#Dash Framework
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Instantiate the Dash Class
#app = DjangoDash('SpectralPlot')

current_dir = os.path.dirname(__file__)

class spectraldataclass():
  def __init__(self, keyname):
    self.responselist={}
    self.responselist['ACIS-S HEG+1 (cy22)']=os.path.join(current_dir,'response/precalc_spec_acistest.pkl')
    self.responselist['Dummy 0.01A (Chandra HEG-like)']=os.path.join(current_dir,'response/precalc_spec_dummyheg.pkl')
    self.responselist['Dummy 5eV (XRISM/Resolve-like)']=os.path.join(current_dir,'response/precalc_spec_dummyresolve.pkl')

    self.curresp = keyname
    self.spectraldata = pickle.load(open(self.responselist[self.curresp], 'rb'))


  def get_spectrum(self, keyname):
    if keyname== self.curresp:
      return self.spectraldata
    else:
      self.curresp = keyname
      self.spectraldata = pickle.load(open(self.responselist[self.curresp], 'rb'))
      return self.spectraldata



curresp='ACIS-S HEG+1 (cy22)'
spectraldataobject = spectraldataclass(curresp)
#Instantiate the Session class
#s = pyatomdb.spectrum.CIESession()

#Setup The PyAtoDB Dynamic Generator Function
#Function for dynamically updating the graphs


def generate_values(temperature_index, units, resp):
    """
    Generates the spectral values to be used in calculated the
    graphical outputs. So far, this accepts the temperature and the
    units defined by the user interface. Lastly, one would be able
    to define the desired response file given by the dropdown menu
    once that portion is completed.


    Parameters:
    temperature (float): The temperature set by the user inteface to be
    fed into the pyatomdb return_spectra method

    units (str): The desired units based on the user's choice of Angstroms
    or keV


    Return:
    binedges (np.ndarray): the bin edges of the emissivity profile calculated by the
    get_response_ebins method. Based on the user-defined units, we convert
    the bins as necessary

    displayspec (np.ndarray): The display spectra of the user-defined system
    """
    #Set the response based on the value returned by the Response
    #Dropdown labeled 'response'
    spectraldata = spectraldataobject.get_spectrum(resp)

    iT=temperature_index
    spec = spectraldata[iT]

    ebins = spectraldata['ebins']

    binunits = units

    #Check the units input by the user. If the units radio
    #value == 'Angstroms', then convert it into the PyAtomDB
    #units identifier
    if binunits == 'A':
        binedges = 12.398425/ebins[::-1]
        displayspec=spec[::-1]

    else: # presumably in keV, so no change
        binedges = ebins
        displayspec=spec

    displayspec = np.append(displayspec, 1e-40)

    return (binedges, displayspec)

#Function used to Generate Stem Plots
def stem_plot(x, y):
    """
    Returns a matplotlib stem plot that is later converted into
    a plotly graph that is fed into the dash routine later.

    Parameters:
    x (array): x coordinates of the stems
    y (array): y coordinates of the stems

    Returns:
    plotly_fig (obj): A plotly figure object that converts the static
    matplotlib stem plot into an interactive plot.
    """
    fig = Figure()
    ax = fig.subplots()

    x = x
    y = y

    ax.stem(x,y)

    plotly_fig = tls.mpl_to_plotly(fig)

    return plotly_fig


temperatures = np.logspace(4,9,51)
temperatures = np.around(temperatures, decimals=-4)

responses = spectraldataobject.responselist.keys()

app.layout = html.Div([
  html.Div([
            html.Div([
            dcc.Slider(
                id='temperature',
                min =4,
                max =9,
                step=0.1,
                value=6,
                marks={4:{'label':'10^4K','style':{'color':'#AA0000'}},
                       5:{'label':'10^5K','style':{'color':'#AA0000'}},
                       6:"10^6K",
                       7:'10^7K',
                       8:'10^8K',
                       9:'10^9K'},

            ),
            html.Label(id='temperature-output-container'),


#            dcc.Dropdown(
#                id='temperature',
#                options=[
#                {'label': np.format_float_scientific(i),
#                'value': i} for i in temperatures
#                ],
#                value=1e6
 #           ),
            html.Label('Spectral Units'),
            dcc.RadioItems(
                id='units',
                options = [
                    {'label': j, 'value':j} for j in ['Angstroms', 'keV']
                ],
                value='Angstroms',
                labelStyle={'display': 'inline-block'},
             ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
            html.Label('Response File'),
            dcc.Dropdown(
                id='response',
                options=[
                {'label': i, 'value': i} for i in responses
                ],
                value='ACIS-S HEG+1 (cy22)',
                ),
            html.Div([
                html.Label('X Axis Type'),
                dcc.RadioItems(
                id='xaxis_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
                ),

                ], style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Y Axis Type'),
                dcc.RadioItems(
                id='yaxis_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
                ),

                ], style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Show Lines'),
                dcc.RadioItems(
                id='show_needleplot',
                options=[{'label': i, 'value': i} for i in ['Yes', 'No']],
                value='Yes',
                labelStyle={'display': 'inline-block'}
                ),

                ], style={'width': '30%', 'display': 'inline-block'}),

    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    dcc.Graph(
        id='atomdb_visual',
        style={
            'height': 700
        }
        )
])

@app.callback(dash.dependencies.Output('temperature-output-container', 'children'),
              [dash.dependencies.Input('temperature','value')])
def update_temperature(value):
  return("Temperature: 10^%.1f K, %.1e K, %.4f keV"%(value, 10**value, 10**value/1000/11604.5))


@app.callback(dash.dependencies.Output('atomdb_visual', 'figure'),
    [dash.dependencies.Input('temperature', 'value'),
    dash.dependencies.Input('response', 'value'),
    dash.dependencies.Input('units', 'value'),
    dash.dependencies.Input('xaxis_type', 'value'),
    dash.dependencies.Input('yaxis_type', 'value'),
    dash.dependencies.Input('show_needleplot','value')])



def update_graph(logtemperature, response, units,
    xaxis_type, yaxis_type, show_needleplot):


    if units == 'Angstroms':
        xaxis = 'Wavelength (%s)'%(units)
        unit = 'A'
    else:
        xaxis = 'Energy (%s)'%(units)
        unit = 'keV'

#    rmf = rmfdict[response]
#    arf = arfdict[response]

    if show_needleplot.lower() =='yes':
      needleplot = True
    else:
      needleplot=False

    temperature=10**logtemperature
    iT = np.argmin(np.abs(np.logspace(4,9,51)-temperature))

    binedges, displayspec = generate_values(iT, unit, response)
    #Draw the traces
    trace1 = go.Scatter(x=binedges, y=displayspec,
            line=dict(
                shape = 'hv',
                color = '#9467bd'
            ),
            mode='lines',
            name='Plot')

    if needleplot:

      spectraldata=spectraldataobject.get_spectrum(response)
    #Get the emissivity information from pyatomdb
#    erange = [min(s.ebins_out), max(s.ebins_out)]
      emis_info = spectraldata['llist'][iT] #s.return_linelist(temperature, erange,specunit='keV',\
                                  #teunit='K', apply_aeff=True, nearest=True)

      max_peak = displayspec.max()


      lines = emis_info
      linemissaeff = lines['Epsilon_Err']
      lines = lines[linemissaeff > 0]
      linemissaeff = linemissaeff[linemissaeff > 0]

#    if (len(lines)>0):
#
#      linemissaeff*= max_peak/max(linemissaeff)

      if len(lines)>1000:
          ind = np.argsort(linemissaeff)[-1000:]
          lines = lines[ind]
          linemissaeff=linemissaeff[ind]

      t1 = time.time()
      ion_symbols = []
      for l in lines:

        ion_symbols.append('<a href="http://www.atomdb.org/Webguide/transition_information.php?lower=%i&upper=%i&z0=%i&z1=%i" target="_blank">%s</a>'%(l['LowerLev'], l['UpperLev'], l['Element'], l['Ion']-1,spectroscopic_name(l['Element'],l['Ion'])))
      t2 = time.time()

      print("Time for generating symbols: %fs"%(t2-t1))

    #peak_mask = np.where(np.logical_and(displayspec<=max_peak,displayspec>=0.5*max_peak))
    #measured_peaks = displayspec[peak_mask]
    #measured_xs = binedges[peak_mask]


    #Find the peaks in the data
#    epeaks = emis[emis['Epsilon']>1e-20]

#    indices = find_peaks(displayspec, distance=10, threshold=1e-25)[0]

    #Generate the stem plot from the data

    #stem_edges

    #stem_edges = [binedges[j] for j in indices]
    #stem_spec = [displayspec[j] for j in indices]

    #Make a list of the ion symbols to be displayed on hover
#    ion_symbols = []
    #spec_aeff = []
    #for eps in stem_spec:
    #    index, aeff_specs = find_nearest(emis, eps)

        #Append the decoded bytes into the ion_symbols list used for
        #the hovertext property later
    #    ion_symbols.append(pyatomdb.atomic.spectroscopic_name(emis_info['Element'][index],emis_info['Ion'][index]))
    #    spec_aeff.append(aeff_specs)


      ion_symbols = np.array(ion_symbols)
    #spec_aeff = np.array(spec_aeff)
    #Make the needle plot via the stem_plot function above

      t1 = time.time()
      if units.lower()=='kev':
#        needle_plot = stem_plot(HC_IN_KEV_A/lines['Lambda'], lines['Epsilon_Err'])
        xvals = HC_IN_KEV_A/lines['Lambda']
      else:
        xvals = lines['Lambda']
#        needle_plot = stem_plot(lines['Lambda'], lines['Epsilon_Err'])
      t2 = time.time()
      print("Time for generating needle_plot: %fs"%(t2-t1))

      trace2 = go.Scatter(x=xvals, y=lines['Epsilon_Err'],
#            line=dict(
#                shape = 'hv',
#                color = '#9467bd'
#            ),
            mode='markers',
            text = ion_symbols)

    #Update each stick with the generated ion symbols found in thhe ion_symbols array
#      needle_plot.update_traces(hovertext=ion_symbols, hoverinfo='text')
#
      data_list = [trace2]
    else:
      data_list = []

    t1 = time.time()
    data_list.append(trace1)
    t2 = time.time()
    print("Time for appending traces: %fs"%(t2-t1))
    print(" There are %i traces"%(len(data_list)))

    #data_list.append(peak_trace)
    #Return the traces into a graph environment
    return {
     'data': data_list,
    'layout': go.Layout(
            xaxis={'title': xaxis, 'type': 'linear' if xaxis_type == 'Linear' else 'log'},
            yaxis={
                'title': 'Emissivity*A<sub>eff</sub> (ph cm<sup>5</sup> s<sup>-1</sup> bin<sup>-1</sup>)',
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
                },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest',
            uirevision = True,
            showlegend=False,
        )
    }

if __name__ == '__main__':
    app.run_server(debug=False)

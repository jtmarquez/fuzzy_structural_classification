from flask import request, jsonify
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
from simpful import *
import pandas as pd

def init_model():
    
    labels = ['Entorno sin contamiación', 'Sistema Estructural/Constructivo', 'Instalación Domiciliaria de Agua Potable & Artefactos',
    'Instalación Domiciliaria de Aguas Servidas & Artefactos', 'Instalación Domiciliaria de Electricidad & Artefactos',
    'Estanqueidad de Envolvente','Calidad del Aire Interior & Ventilación', 'Instalación Domiciliaria de Gas & Artefactos', 'Protección contra Ingreso No Autorizado',
    'Acabado y Terminaciones de Elementos Constructivos', 'Mobiliario & Equipamiento Genérico']
    reglas_modelo = """resultado;P1;P2;P3;P4;P5;P6;P7;P8;P9;P10;P11
    IC_C;P1_E;P2_E;P3_F;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_E;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_D;P3_F;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_E;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_E;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_E;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_E;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_E;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_E;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_E;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_E;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_E;P2_D;P3_F;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_E;P3_F;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_C;P1_D;P2_D;P3_E;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_C;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_D;P7_C;None;None;None;None
    IC_Inad;P1_E;P2_E;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_C;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_C;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_E;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_F;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_D;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_D;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_F;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_C;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_E;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_C;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_E;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_C;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_E;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_C;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_E;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_C;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_E;P7_C;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_C;P7_C;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_D;P5_D;P6_D;P7_C;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_F;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_D;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_D;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_F;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_C;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_C;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_E;P2_D;P3_E;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_D;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_C;P2_D;P3_E;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_C;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_C;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_E;P5_D;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_D;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_E;P3_E;P4_D;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_C;P3_E;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_D;P5_C;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_D;P5_E;P6_D;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_D;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_D;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_D;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_F;P4_D;P5_D;P6_D;P7_C;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_D;P4_D;P5_D;P6_D;P7_C;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_E;P5_D;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_C;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_E;P5_D;P6_C;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_C;P5_D;P6_E;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_D;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_C;P6_C;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_C;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_B;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_C;P6_C;P7_B;None;None;None;None
    IC_Insf;P1_B;P2_C;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_B;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_B;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_C;P6_B;P7_C;None;None;None;None
    IC_Insf;P1_A;P2_C;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_A;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_A;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_C;P6_A;P7_C;None;None;None;None
    IC_Insf;P1_B;P2_B;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_B;P2_C;P3_D;P4_B;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_B;P2_C;P3_D;P4_C;P5_C;P6_B;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_B;P3_D;P4_B;P5_C;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_B;P3_D;P4_C;P5_C;P6_B;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_B;P5_C;P6_B;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_D;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_F;P4_C;P5_E;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_D;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_F;P4_C;P5_D;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_E;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_C;P6_C;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_F;P4_C;P5_C;P6_C;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_D;P6_C;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_E;P6_C;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_C;P4_C;P5_B;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_B;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_B;P4_C;P5_D;P6_C;P7_C;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_C;P4_C;P5_C;P6_C;P7_B;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_E;P4_C;P5_C;P6_C;P7_B;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_C;P4_C;P5_C;P6_C;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_B;P6_C;P7_B;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_D;P6_C;P7_B;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_B;P6_C;P7_D;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_D;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_C;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_B;P6_B;P7_C;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_D;P4_B;P5_C;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_D;P4_B;P5_B;P6_B;P7_C;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_C;P6_B;P7_C;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_B;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_A;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_B;P6_B;P7_A;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_A;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_C;P2_B;P3_C;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_C;P3_C;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_C;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_B;P6_C;P7_B;None;None;None;None
    IC_Suf;P1_C;P2_B;P3_D;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_C;P2_B;P3_C;P4_B;P5_C;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_C;P2_B;P3_C;P4_B;P5_B;P6_B;P7_C;None;None;None;None
    IC_Suf;P1_B;P2_C;P3_D;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_C;P3_C;P4_B;P5_C;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_C;P3_C;P4_B;P5_B;P6_B;P7_C;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_D;P4_C;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_C;P5_C;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_C;P5_B;P6_B;P7_C;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_D;P4_B;P5_B;P6_C;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_C;P6_C;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_B;P6_C;P7_C;None;None;None;None
    IC_Suf;P1_A;P2_B;P3_C;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_A;P3_C;P4_B;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_A;P5_B;P6_B;P7_B;None;None;None;None
    IC_Suf;P1_B;P2_B;P3_C;P4_B;P5_B;P6_A;P7_B;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_B;P4_A;P5_A;P6_A;P7_A;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_C;P4_A;P5_A;P6_A;P7_A;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_B;P4_A;P5_A;P6_A;P7_A;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_A;P4_A;P5_A;P6_A;P7_A;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_B;P4_A;P5_B;P6_A;P7_A;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_A;P4_A;P5_B;P6_A;P7_A;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_B;P4_A;P5_A;P6_A;P7_B;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_A;P4_A;P5_A;P6_A;P7_B;None;None;None;None
    IC_Suf;P1_A;P2_A;P3_C;P4_A;P5_C;P6_A;P7_C;None;None;None;None
    IC_Suf;P1_A;P2_A;P3_B;P4_A;P5_C;P6_A;P7_C;None;None;None;None
    IC_Exc;P1_A;P2_A;P3_B;P4_A;P5_B;P6_A;P7_B;None;None;None;None
    IC_C;P1_E;P2_E;P3_F;P4_E;P5_E;P6_E;P7_D;None;None;None;None
    IC_Inad;P1_D;P2_D;P3_E;P4_D;P5_D;P6_D;P7_D;None;None;None;None
    IC_Insf;P1_C;P2_C;P3_D;P4_C;P5_C;P6_C;P7_C;None;None;None;None
    IC_Inad;None;None;None;None;None;None;None;None;P9_E;P10_E;P11_D
    IC_Inad;None;None;None;None;None;None;None;None;P9_E;P10_E;P11_C
    IC_Inad;None;None;None;None;None;None;None;None;P9_E;P10_E;P11_B
    IC_Inad;None;None;None;None;None;None;None;None;P9_E;P10_E;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_D;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_D;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_D;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_D;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_C;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_C;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_C;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_C;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_B;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_B;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_B;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_B;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_A;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_A;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_A;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_E;P10_A;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_E;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_E;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_E;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_E;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_E;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_E;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_E;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_E;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_B;P10_E;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_B;P10_E;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_B;P10_E;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_B;P10_E;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_A;P10_E;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_A;P10_E;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_A;P10_E;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_A;P10_E;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_D;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_D;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_D;P11_B
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_D;P11_A
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_C;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_B;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_A;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_D;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_B;P10_D;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_A;P10_D;P11_D
    IC_Insf;None;None;None;None;None;None;None;None;P9_D;P10_C;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_D;P11_C
    IC_Insf;None;None;None;None;None;None;None;None;P9_C;P10_C;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_D;P10_C;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_D;P10_C;P11_A
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_D;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_D;P11_A
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_C;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_B;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_A;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_A;P10_C;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_A;P10_B;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_A;P10_A;P11_D
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_C;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_C;P11_A
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_C;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_A;P10_C;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_B;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_A;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_C;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_B;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_B;P11_A
    IC_Suf;None;None;None;None;None;None;None;None;P9_C;P10_A;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_C;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_C;P11_A
    IC_Suf;None;None;None;None;None;None;None;None;P9_A;P10_C;P11_B
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_B;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_A;P10_B;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_B;P11_C
    IC_Suf;None;None;None;None;None;None;None;None;P9_B;P10_A;P11_C
    IC_Exc;None;None;None;None;None;None;None;None;P9_C;P10_A;P11_A
    IC_Exc;None;None;None;None;None;None;None;None;P9_A;P10_C;P11_A
    IC_Exc;None;None;None;None;None;None;None;None;P9_A;P10_A;P11_C
    IC_Exc;None;None;None;None;None;None;None;None;P9_B;P10_B;P11_B
    IC_Exc;None;None;None;None;None;None;None;None;P9_B;P10_B;P11_A
    IC_Exc;None;None;None;None;None;None;None;None;P9_A;P10_B;P11_B
    IC_Exc;None;None;None;None;None;None;None;None;P9_B;P10_A;P11_B
    IC_Exc;None;None;None;None;None;None;None;None;P9_B;P10_A;P11_A
    IC_Exc;None;None;None;None;None;None;None;None;P9_A;P10_B;P11_A
    IC_Exc;None;None;None;None;None;None;None;None;P9_A;P10_A;P11_B
    IC_Exc;None;None;None;None;None;None;None;None;P9_A;P10_A;P11_A
    IC_Insf;None;None;P3_E;P4_C;P5_C;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_C;P5_C;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_C;P5_C;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_C;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_C;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_C;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_C;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_B;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_A;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_C;P5_C;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_C;P5_B;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_C;P5_A;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_C;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_B;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_A;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_C;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_B;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_B;P5_A;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_C;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_B;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_A;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_C;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_B;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_E;P4_A;P5_A;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_D;P4_C;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_C;P4_C;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_B;P4_C;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_A;P4_C;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_A;P4_B;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_D;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_D;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_D;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_A;P4_B;P5_D;None;None;P8_B;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_C;P4_A;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_B;P4_A;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_A;P4_A;P5_D;None;None;P8_C;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_D;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_C;P4_A;P5_D;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_B;P4_A;P5_D;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_A;P4_A;P5_D;None;None;P8_A;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_A;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_A;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_A;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_A;P4_A;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_A;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_A;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_A;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_A;P4_A;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_A;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_A;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_B;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_B;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_C;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_D;P4_A;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_C;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_C;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_B;P5_A;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_C;P5_B;None;None;P8_D;None;None;None
    IC_Insf;None;None;P3_B;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Suf;None;None;P3_D;P4_B;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_D;P4_B;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_D;P4_A;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_D;P4_B;P5_B;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_D;P4_A;P5_B;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_D;P4_B;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_C;P4_C;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_C;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_C;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_C;P5_A;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_C;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_B;P5_C;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_A;P4_B;P5_C;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_C;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_B;P4_B;P5_C;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_A;P4_B;P5_C;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_B;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_B;P4_B;P5_B;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_A;P4_B;P5_B;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_A;P4_A;P5_B;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_A;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_B;P4_B;P5_A;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_A;P4_A;P5_A;None;None;P8_C;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_A;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_A;P4_A;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_B;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_A;P4_B;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_C;P4_B;P5_B;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_C;P4_A;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_A;P5_C;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_A;P5_C;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_B;P4_A;P5_B;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_A;P5_B;None;None;P8_A;None;None;None
    IC_Suf;None;None;P3_B;P4_A;P5_A;None;None;P8_B;None;None;None
    IC_Suf;None;None;P3_B;P4_A;P5_B;None;None;P8_B;None;None;None
    IC_Exc;None;None;P3_C;P4_A;P5_A;None;None;P8_A;None;None;None
    IC_Exc;None;None;P3_B;P4_A;P5_A;None;None;P8_A;None;None;None
    IC_Exc;None;None;P3_A;P4_B;P5_A;None;None;P8_A;None;None;None
    IC_Exc;None;None;P3_A;P4_A;P5_B;None;None;P8_A;None;None;None
    IC_Exc;None;None;P3_A;P4_A;P5_A;None;None;P8_B;None;None;None
    IC_Exc;None;None;P3_A;P4_C;P5_A;None;None;P8_A;None;None;None
    IC_Exc;None;None;P3_A;P4_A;P5_C;None;None;P8_A;None;None;None
    IC_Exc;None;None;P3_A;P4_A;P5_A;None;None;P8_C;None;None;None
    IC_Exc;None;None;P3_A;P4_A;P5_A;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_A;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_A;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_B;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_B;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_C;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_C;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_A;P4_A;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_B;P4_A;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_C;P4_A;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_D;P4_A;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_A;P4_B;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_B;P4_B;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_C;P4_B;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_D;P4_B;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_A;P4_C;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_B;P4_C;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_C;P4_C;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_D;P4_C;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_D;None;None;P8_C;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_D;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_D;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_B;P5_D;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_B;P5_D;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_E;P4_B;P5_D;None;None;P8_C;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_C;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_B;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_A;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_D;P4_D;P5_D;None;None;P8_C;None;None;None
    IC_Inad;None;None;P3_D;P4_D;P5_D;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_D;P4_D;P5_D;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_C;P4_D;P5_D;None;None;P8_C;None;None;None
    IC_Inad;None;None;P3_C;P4_D;P5_D;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_C;P4_D;P5_D;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_B;P4_D;P5_D;None;None;P8_C;None;None;None
    IC_Inad;None;None;P3_B;P4_D;P5_D;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_B;P4_D;P5_D;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_D;None;None;P8_C;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_D;None;None;P8_B;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_D;None;None;P8_A;None;None;None
    IC_Inad;None;None;P3_D;P4_D;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_C;P4_D;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_B;P4_D;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_C;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_B;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_A;P5_D;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_C;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_B;None;None;P8_D;None;None;None
    IC_Inad;None;None;P3_E;P4_D;P5_A;None;None;P8_D;None;None;None
    IC_C;None;None;P3_F;P4_D;P5_D;None;None;P8_D;None;None;None
    IC_C;None;None;P3_E;P4_E;P5_D;None;None;P8_D;None;None;None
    IC_C;None;None;P3_E;P4_D;P5_E;None;None;P8_D;None;None;None
    IC_C;None;None;P3_E;P4_D;P5_D;None;None;P8_E;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_A;None;None;P8_A;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_A;None;None;P8_B;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_A;None;None;P8_C;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_A;None;None;P8_D;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_B;None;None;P8_A;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_B;None;None;P8_B;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_B;None;None;P8_C;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_B;None;None;P8_D;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_C;None;None;P8_A;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_C;None;None;P8_B;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_C;None;None;P8_C;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_C;None;None;P8_D;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_D;None;None;P8_A;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_D;None;None;P8_B;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_D;None;None;P8_C;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_D;None;None;P8_D;None;None;None
    IC_C;None;None;P3_E;P4_E;P5_E;None;None;P8_D;None;None;None
    IC_C;None;None;P3_D;P4_E;P5_E;None;None;P8_D;None;None;None
    IC_C;None;None;P3_C;P4_E;P5_E;None;None;P8_D;None;None;None
    IC_C;None;None;P3_B;P4_E;P5_E;None;None;P8_D;None;None;None
    IC_C;None;None;P3_A;P4_E;P5_E;None;None;P8_D;None;None;None
    IC_C;None;None;P3_E;P4_E;P5_E;None;None;P8_C;None;None;None
    IC_C;None;None;P3_D;P4_E;P5_E;None;None;P8_C;None;None;None
    IC_C;None;None;P3_C;P4_E;P5_E;None;None;P8_C;None;None;None
    IC_C;None;None;P3_B;P4_E;P5_E;None;None;P8_C;None;None;None
    IC_C;None;None;P3_A;P4_E;P5_E;None;None;P8_C;None;None;None
    IC_C;None;None;P3_E;P4_E;P5_E;None;None;P8_B;None;None;None
    IC_C;None;None;P3_D;P4_E;P5_E;None;None;P8_B;None;None;None
    IC_C;None;None;P3_C;P4_E;P5_E;None;None;P8_B;None;None;None
    IC_C;None;None;P3_B;P4_E;P5_E;None;None;P8_B;None;None;None
    IC_C;None;None;P3_A;P4_E;P5_E;None;None;P8_B;None;None;None
    IC_C;None;None;P3_E;P4_D;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_D;P4_D;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_C;P4_D;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_B;P4_D;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_E;P4_C;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_D;P4_C;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_C;P4_C;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_B;P4_C;P5_E;None;None;P8_E;None;None;None
    IC_C;None;None;P3_F;P4_E;P5_E;None;None;P8_E;None;None;None"""
    trims = [
            [ #I1
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10]
            ],
            [ #I2
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I3
                [0, 0, 1.95],
                [1.45, 2.5, 3.55],
                [3.05, 4.2, 5.25],
                [4.75, 5.8, 6.95],
                [6.45, 7.5, 8.55],
                [8.05, 10, 10],
            ],
            [ #I4
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I5
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I6
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I7
                [0, 0, 3],
                [2, 3.75, 5.5],
                [4.5, 6.25, 8],
                [7, 10, 10],
            ],
            [ #I8
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I9
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I10
                [0, 0, 2.5],
                [1.5, 3, 4.5],
                [3.5, 5, 6.5],
                [5.5, 7, 8.5],
                [7.5, 10, 10],
            ],
            [ #I11
                [0, 0, 3],
                [2, 3.75, 5.5],
                [4.5, 6.25, 8],
                [7, 10, 10],
            ]
        ]
    categories = ['F', 'E', 'D', 'C', 'B', 'A'][::-1]
    labels_num = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11']
    consecuent_categories = ['IC_C', 'IC_Inad', 'IC_Insf', 'IC_Suf', 'IC_Exc']
    trims_consecuent = [[0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 8], [8, 9, 10]]
    FS = FuzzySystem()
    sets = list()
    
    external_index = 0
    for var_trim_set in trims:
        internal_set = list()
        internal_index = 0
        for trim_set in var_trim_set[::-1]:
            internal_set.append(FuzzySet(function=Triangular_MF(a=trim_set[0],b=trim_set[1],c=trim_set[2]), term=categories[internal_index]))
            internal_index += 1
        FS.add_linguistic_variable(labels_num[external_index], LinguisticVariable(internal_set, concept=labels[external_index], universe_of_discourse=[0,10]))
        sets.append(internal_set)
        external_index += 1
    cat_index = 0

    consecuent_fuzzy_set = list()
    for var_consequent_trim in trims_consecuent:
        cat = consecuent_categories[cat_index].split("_")[1]
        consecuent_fuzzy_set.append(FuzzySet(function=Triangular_MF(a=var_consequent_trim[0],b=var_consequent_trim[1],c=var_consequent_trim[2]), term=cat))
        cat_index += 1
    FS.add_linguistic_variable("IC", LinguisticVariable(consecuent_fuzzy_set, concept="IC", universe_of_discourse=[0,10]))

    df = pd.DataFrame([x.split(';') for x in reglas_modelo.split('\n')[1:]], columns=[x for x in reglas_modelo.split('\n')[0].split(';')])

    cols = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11']
    reglas = list()
    for index, row in df.iterrows():
        rule = False
        regla = list()
        for row_item in row[cols]:
            if row_item != 'null' and row_item != None and row_item != 'None':
                regla.append(row_item.split("_"))
        regla_2 = list(map(lambda x: f"({x[0]} IS {x[1]})", regla))
        #regla_t = [row[cols]]
        _ = "IF "+ " AND ".join(regla_2)
        status_response = row['resultado'].split("_")[-1]
        _ += F" THEN (IC IS {status_response})"
        reglas.append(_)

    FS.add_rules(reglas)
    return FS

class FuzzModel:
    def __init__(self):
        self.FS = init_model()

    def compute(self, input_args):
        for variable, input_val in input_args.items():
            self.FS.set_variable(variable, input_val)
        inf_value = self.FS.inference()['IC']
        if inf_value >= 0 and inf_value <=2:
            categoria_inf_value = 'C'
        elif inf_value > 2 and inf_value <= 4:
            categoria_inf_value = 'Inad'
        elif inf_value > 4 and inf_value <= 6:
            categoria_inf_value = 'Insf'
        elif inf_value > 6 and inf_value <= 8:
            categoria_inf_value = 'Suf'
        else:
            categoria_inf_value = 'Exc'
        info = {
            'valor': inf_value,
            'categoria': categoria_inf_value,
        }
        return info

app = Flask(__name__)
#app.config['DEBUG'] = True
api = Api(app)
fuzz_model = FuzzModel()

@app.route('/api/fuzzify', methods = ['POST'])
def api_fuzzify():
    json_data = request.json

    if len(json_data) != 11:
        return "Error: no se entregaron todos los argumentos necesarios:"
    else:
        inf_val = fuzz_model.compute(json_data)
        return jsonify(inf_val)

app.run()


    

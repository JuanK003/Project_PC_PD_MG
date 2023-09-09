import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: FirebaseOptions(
        apiKey: "AIzaSyBVMbDxfHz4wtcCZd1tVLsngwOWTNTXltE",
        authDomain: "pruebadjango-cc7f1.firebaseapp.com",
        databaseURL: "https://pruebadjango-cc7f1-default-rtdb.firebaseio.com",
        projectId: "pruebadjango-cc7f1",
        storageBucket: "pruebadjango-cc7f1.appspot.com",
        messagingSenderId: "511727626220",
        appId: "1:511727626220:web:1b2a2a1e849a9f0e03c2c9",
        measurementId: "G-C003HSYZVR"),
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
      theme: ThemeData(
        appBarTheme: AppBarTheme(
          color: Color(0xFF4D82BC), // Color de fondo de la barra de navegación
        ),
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final DatabaseReference databaseReference =
      FirebaseDatabase.instance.reference().child('Tournament');
  Map<String, dynamic>? tournamentData;

  @override
  void initState() {
    super.initState();
    readData();
  }

  void readData() {
    databaseReference.once().then((DatabaseEvent event) {
      final snapshot = event.snapshot;
      final data = snapshot.value as Map<dynamic, dynamic>?;
      if (data != null) {
        setState(() {
          tournamentData = Map<String, dynamic>.from(data);
        });
      } else {
        setState(() {
          tournamentData = {'error': 'Ningún dato encontrado'};
        });
      }
    }).catchError((error) {
      setState(() {
        tournamentData = {'error': 'Error al leer datos: $error'};
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Lectura de Datos Firebase'),
      ),
      body: Container(
        color: Color(0xFF005187), // Color de fondo
        child: Center(
          child: tournamentData != null
              ? ListView.builder(
                  itemCount: tournamentData!.length,
                  itemBuilder: (context, index) {
                    final tournament = tournamentData!.values.elementAt(index);
                    return Card(
                      elevation: 4,
                      margin: EdgeInsets.all(8),
                      color: Color(0xFFC4DAFA), // Color de las tarjetas
                      shape: RoundedRectangleBorder(
                        borderRadius:
                            BorderRadius.circular(15.0), // Bordes redondeados
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                                'Nombre del torneo: ${tournament['name_tournament']}',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF021D34), // Color del texto
                                )),
                            SizedBox(height: 8),
                            Text('Deporte: ${tournament['sport']}',
                                style: TextStyle(
                                  color: Color(0xFF021D34), // Color del texto
                                )),
                            Text('Fecha de Inicio: ${tournament['start_date']}',
                                style: TextStyle(
                                  color: Color(0xFF021D34), // Color del texto
                                )),
                            Text(
                                'Fecha de Finalización: ${tournament['end_date']}',
                                style: TextStyle(
                                  color: Color(0xFF021D34), // Color del texto
                                )),
                            Text('ID del Usuario: ${tournament['id_user']}',
                                style: TextStyle(
                                  color: Color(0xFF021D34), // Color del texto
                                )),
                          ],
                        ),
                      ),
                    );
                  },
                )
              : Text('No se encontraron datos'),
        ),
      ),
    );
  }
}

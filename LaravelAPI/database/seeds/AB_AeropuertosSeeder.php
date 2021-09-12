<?php

use Illuminate\Database\Seeder;

class AB_AeropuertosSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto de Madrid-Barajas Adolfo Suárez',
            'ciudad' => 'Madrid',
            'pais' => 'España',
            'siglas' => 'MAD',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto de Berlín-Schönefeld',
            'ciudad' => 'Berlín',
            'pais' => 'Alemania',
            'siglas' => 'SFX',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional Rey Abdulaziz',
            'ciudad' => 'Yeda',
            'pais' => 'Arabia Saudita',
            'siglas' => 'JED',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeroparque Internacional Jorge Newbery',
            'ciudad' => 'Buenos Aires',
            'pais' => 'Argentina',
            'siglas' => 'AEP',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Canberra',
            'ciudad' => 'Canberra',
            'pais' => 'Australia',
            'siglas' => 'CBR',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de São Paulo-Guarulhos',
            'ciudad' => 'Guarulhos',
            'pais' => 'Brasil',
            'siglas' => 'GRU',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional Toronto Pearson',
            'ciudad' => 'Toronto',
            'pais' => 'Canada',
            'siglas' => 'YYZ',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Pekín',
            'ciudad' => 'Pekín',
            'pais' => 'China',
            'siglas' => 'PEK',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Incheon',
            'ciudad' => 'Incheon',
            'pais' => 'Corea del Sur',
            'siglas' => 'ICN',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Atlanta',
            'ciudad' => 'Atlanta',
            'pais' => 'EEUU',
            'siglas' => 'ATL',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto de París-Charles de Gaulle',
            'ciudad' => 'París',
            'pais' => 'Francia',
            'siglas' => 'CDG',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional Indira Gandhi',
            'ciudad' => 'Delhi',
            'pais' => 'India',
            'siglas' => 'DEL',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional Soekarno-Hatta',
            'ciudad' => 'Tangerang',
            'pais' => 'Indonesia',
            'siglas' => 'CGK',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto de Roma-Fiumicino',
            'ciudad' => 'Roma',
            'pais' => 'Italia',
            'siglas' => 'FCO',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Narita',
            'ciudad' => 'Narita',
            'pais' => 'Japón',
            'siglas' => 'NRT',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de la Ciudad de México',
            'ciudad' => 'Ciudad de México',
            'pais' => 'México',
            'siglas' => 'MEX',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto de Londres-Heathrow',
            'ciudad' => 'Londres',
            'pais' => 'Reino Unido',
            'siglas' => 'LHR',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Moscú-Domodédovo',
            'ciudad' => 'Moscú',
            'pais' => 'Rusia',
            'siglas' => 'DME',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional de Johannesburgo-Oliver Reginald Tambo',
            'ciudad' => 'Johannesburgo',
            'pais' => 'Sudáfrica',
            'siglas' => 'JNB',
        ]);

        DB::table('aeropuertos')->insert([
            'nombre' => 'Aeropuerto Internacional Atatürk',
            'ciudad' => 'Estambul',
            'pais' => 'Turquía',
            'siglas' => 'ISL',
        ]);
    }
}

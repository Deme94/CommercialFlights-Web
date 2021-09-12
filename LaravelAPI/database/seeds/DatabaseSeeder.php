<?php

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // $this->call(UserSeeder::class);
        $this->call(AA_AerolineasSeeder::class);
        $this->call(AB_AerolineasSeeder::class);
        $this->call(AC_AerolineasSeeder::class);
        $this->call(AD_AerolineasSeeder::class);
        $this->call(BA_ReviewsAeropuertosSeeder::class);
        $this->call(BB_ReviewsAerolineasSeeder::class);
        $this->call(BC_ReviewsVuelosSeeder::class);

    }
}

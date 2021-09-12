<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateReviewsVuelosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('reviews_vuelos', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            # keys
            $table->integer('id_vuelo')->unsigned();
            $table->foreign('id_vuelo')->references('id')->on('vuelos');
            # campos propios
            $table->text('nombre')->nullable();
            $table->longText('opinion')->nullable();
            $table->dateTime('date_time');
            $table->float('compound');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('reviews_vuelos');
    }
}

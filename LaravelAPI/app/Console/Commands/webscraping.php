<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

class webscraping extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'webscraping:everyday';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Ejecuta los ficheros python Web Scrapers, una vez al día';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->line('webscraping');
        $this->line(shell_exec(storage_path("/ejecutables/Main.py")));
    }
}

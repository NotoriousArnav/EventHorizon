<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('ticket_types', function (Blueprint $table) {
            $table->id();
            $table->foreignId('event_id')->constrained()->onDelete('cascade');
            $table->string('name');
            $table->text('description')->nullable();
            $table->decimal('price', 10, 2)->default(0);
            $table->string('currency', 3)->default('USD');
            $table->integer('quantity_total')->nullable();
            $table->integer('quantity_available')->nullable();
            $table->timestamp('sales_start')->nullable();
            $table->timestamp('sales_end')->nullable();
            $table->boolean('is_free')->default(true);
            $table->boolean('requires_approval')->default(false);
            $table->integer('sort_order')->default(0);
            $table->timestamps();
            
            $table->index('event_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('ticket_types');
    }
};

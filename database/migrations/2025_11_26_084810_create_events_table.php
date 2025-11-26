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
        Schema::create('events', function (Blueprint $table) {
            $table->id();
            $table->string('organizer_id')->index();
            $table->foreignId('community_id')->nullable()->constrained()->onDelete('set null');
            $table->string('title');
            $table->string('slug')->unique();
            $table->text('description')->nullable();
            $table->string('cover_image_url')->nullable();
            $table->string('location')->nullable();
            $table->enum('location_type', ['online', 'physical', 'hybrid'])->default('physical');
            $table->timestamp('start_datetime');
            $table->timestamp('end_datetime');
            $table->string('timezone')->default('UTC');
            $table->integer('capacity')->nullable();
            $table->enum('status', ['draft', 'published', 'cancelled', 'ended'])->default('draft');
            $table->enum('visibility', ['public', 'unlisted', 'private'])->default('public');
            $table->timestamps();
            
            $table->index(['status', 'visibility']);
            $table->index('start_datetime');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('events');
    }
};

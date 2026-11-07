<?php
/**
 * kamir.si – čiščenje BMP slik v medijski knjižnici.
 *
 * Zagon na strežniku (v korenu WordPressa) z WP-CLI:
 *
 *   wp eval-file kamir-bmp-cleanup.php dry-run              # samo izpiše, kaj bi naredil
 *   wp eval-file kamir-bmp-cleanup.php delete-unused        # izbriše 68 neuporabljenih priponk (.bmp + .webp dvojnico)
 *   wp eval-file kamir-bmp-cleanup.php convert              # priponke v uporabi preusmeri na .webp in izbriše .bmp
 *   wp eval-file kamir-bmp-cleanup.php convert dry-run      # kombinacija: konverzija samo na suho
 *
 * Pred zagonom naredi varnostno kopijo baze in mape wp-content/uploads!
 * Po zagonu počisti LiteSpeed Cache: wp litespeed-purge all
 */

if ( ! defined( 'WP_CLI' ) || ! WP_CLI ) {
	die( "Zaženi z WP-CLI: wp eval-file kamir-bmp-cleanup.php <delete-unused|convert> [dry-run]\n" );
}

$dry_run       = in_array( 'dry-run', $args, true );
$delete_unused = in_array( 'delete-unused', $args, true );
$convert       = in_array( 'convert', $args, true );

if ( ! $delete_unused && ! $convert && ! $dry_run ) {
	WP_CLI::error( 'Podaj način: delete-unused, convert ali dry-run.' );
}
if ( $dry_run && ! $delete_unused && ! $convert ) {
	$delete_unused = true;
	$convert       = true;
}

/*
 * Priponke BMP, ki 7. 11. 2026 niso bile niti glavna niti galerijska slika
 * nobenega objavljenega izdelka in se njihovo ime ne pojavi na nobeni strani
 * (glej bmp-neuporabljene.csv).
 */
$unused_ids = array(
	8927, 8947, 8974, 8981, 10326, 10439, 10514, 10515, 10516, 10518, 10519, 10520, 10521,
	10523, 10524, 10530, 10531, 10532, 10533, 10534, 10535, 10540, 10541, 10543, 10570, 10582,
	10584, 11004, 11006, 11007, 11009, 11010, 11338, 11394, 11395, 11594, 11642, 11734, 11736,
	11789, 11916, 11917, 11918, 11922, 11923, 11924, 11930, 11931, 11932, 11933, 11948, 11958,
	12049, 12055, 12056, 12058, 12060, 12061, 12206, 12220, 12258, 12270, 12293, 12294, 12454,
	12812, 12813, 13856,
);

$uploads  = wp_upload_dir();
$basedir  = trailingslashit( $uploads['basedir'] );
$baseurl  = trailingslashit( $uploads['baseurl'] );
$freed    = 0;

function kamir_webp_twin( $bmp_path ) {
	return preg_replace( '/\.bmp$/i', '.webp', $bmp_path );
}

/* ---------- 1) Brisanje neuporabljenih priponk ---------- */
if ( $delete_unused ) {
	WP_CLI::log( '== Neuporabljene BMP priponke ==' );
	foreach ( $unused_ids as $id ) {
		$post = get_post( $id );
		if ( ! $post || 'attachment' !== $post->post_type ) {
			WP_CLI::warning( "#$id ne obstaja več – preskočim." );
			continue;
		}
		if ( 'image/bmp' !== $post->post_mime_type ) {
			WP_CLI::warning( "#$id ni več BMP ({$post->post_mime_type}) – preskočim." );
			continue;
		}
		// Varovalka: če je priponka medtem postala glavna/galerijska slika kakšnega izdelka, je ne brišemo.
		$as_thumb = get_posts( array( 'post_type' => 'any', 'post_status' => 'any', 'fields' => 'ids', 'posts_per_page' => 1, 'meta_key' => '_thumbnail_id', 'meta_value' => $id ) );
		$in_gal   = get_posts( array( 'post_type' => 'product', 'post_status' => 'any', 'fields' => 'ids', 'posts_per_page' => 1, 'meta_query' => array( array( 'key' => '_product_image_gallery', 'value' => '(^|,)' . $id . '(,|$)', 'compare' => 'REGEXP' ) ) ) );
		if ( $as_thumb || $in_gal ) {
			WP_CLI::warning( "#$id je v uporabi (izdelek " . implode( ',', array_merge( $as_thumb, $in_gal ) ) . ') – preskočim.' );
			continue;
		}
		$file = get_attached_file( $id );
		$webp = kamir_webp_twin( $file );
		$size = ( $file && file_exists( $file ) ? filesize( $file ) : 0 ) + ( file_exists( $webp ) ? filesize( $webp ) : 0 );
		WP_CLI::log( ( $dry_run ? '[suho] ' : '' ) . "briši #$id " . str_replace( $basedir, '', $file ) . ' (+ .webp)' );
		if ( ! $dry_run ) {
			if ( false === wp_delete_attachment( $id, true ) ) {
				WP_CLI::warning( "#$id: wp_delete_attachment ni uspel." );
				continue;
			}
			if ( file_exists( $webp ) ) {
				@unlink( $webp );
			}
		}
		$freed += $size;
	}
}

/* ---------- 2) Konverzija priponk v uporabi: .bmp -> .webp ---------- */
if ( $convert ) {
	WP_CLI::log( '== BMP priponke v uporabi -> preusmeritev na .webp ==' );
	$ids = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'any',
		'post_mime_type' => 'image/bmp',
		'fields'         => 'ids',
		'posts_per_page' => -1,
	) );
	$ids = array_diff( $ids, $unused_ids );
	WP_CLI::log( count( $ids ) . ' priponk za konverzijo.' );

	foreach ( $ids as $id ) {
		$bmp = get_attached_file( $id );
		if ( ! $bmp || ! preg_match( '/\.bmp$/i', $bmp ) ) {
			WP_CLI::warning( "#$id: pripeta datoteka ni .bmp ($bmp) – preskočim." );
			continue;
		}
		$webp = kamir_webp_twin( $bmp );
		if ( ! file_exists( $webp ) ) {
			WP_CLI::warning( "#$id: ni .webp dvojnice za " . str_replace( $basedir, '', $bmp ) . ' – preskočim (BMP ostane).' );
			continue;
		}
		$rel_webp = str_replace( $basedir, '', $webp );
		WP_CLI::log( ( $dry_run ? '[suho] ' : '' ) . "#$id -> $rel_webp, briši .bmp" );
		if ( $dry_run ) {
			$freed += file_exists( $bmp ) ? filesize( $bmp ) : 0;
			continue;
		}

		// Priponka naj kaže na .webp.
		update_attached_file( $id, $webp );
		wp_update_post( array(
			'ID'             => $id,
			'post_mime_type' => 'image/webp',
			'guid'           => $baseurl . $rel_webp,
		) );

		// Metapodatki + pomanjšane različice (BMP jih ni imel).
		$meta = wp_generate_attachment_metadata( $id, $webp );
		if ( empty( $meta ) || is_wp_error( $meta ) ) {
			$dim  = @getimagesize( $webp );
			$meta = array( 'file' => $rel_webp, 'width' => $dim ? $dim[0] : 0, 'height' => $dim ? $dim[1] : 0, 'filesize' => filesize( $webp ), 'sizes' => array(), 'image_meta' => array() );
			WP_CLI::warning( "#$id: pomanjšanih različic ni bilo mogoče ustvariti (strežnik brez WebP podpore v GD/Imagick?) – shranjeni osnovni metapodatki." );
		}
		wp_update_attachment_metadata( $id, $meta );

		if ( file_exists( $bmp ) ) {
			$freed += filesize( $bmp );
			@unlink( $bmp );
		}
	}
}

WP_CLI::success( sprintf( '%s Sproščeno: %.1f MB', $dry_run ? '(suhi tek)' : 'Končano.', $freed / 1048576 ) );
if ( ! $dry_run ) {
	WP_CLI::log( 'Zdaj počisti predpomnilnik: wp litespeed-purge all' );
}
